// The admin portal API. One function, routed by the last part of the path:
//
//   POST /api/admin/login     {email, password}        sign in (sets the cookie)
//   POST /api/admin/logout                              sign out
//   GET  /api/admin/me                                  who is signed in
//   GET  /api/admin/content?path=content/…json          a content file, fresh from GitHub
//   PUT  /api/admin/content   {path, data, sha, message} save it (commits to GitHub)
//   DELETE /api/admin/content {path, sha}               delete a Journal post
//   GET  /api/admin/posts                               every Journal post (title, date, draft)
//   POST /api/admin/upload    {name, data}              upload a photo (base64)
//   GET  /api/admin/events                              every event (title, date, draft)
//   GET  /api/admin/leads     POST {row, status}        event enquiries from the Google Sheet
//   GET  /api/admin/status                              is the last change live yet?
const crypto = require('crypto');
const A = require('./_lib/admin');

// A few wrong passwords in a row lock sign-in for a while (per server instance).
const tries = new Map();

async function login(req, res) {
  if (req.method !== 'POST') return A.send(res, 405, { ok: false });
  const ip = String(req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'x';
  const t = tries.get(ip) || { n: 0, until: 0 };
  if (t.until > Date.now()) return A.send(res, 429, { ok: false, error: 'Too many attempts. Try again in 15 minutes.' });
  const { email, password } = await A.readJson(req, 10000);
  const okEmail = String(email || '').trim().toLowerCase() === String(process.env.ADMIN_EMAIL || '').toLowerCase();
  const okPass = A.checkPassword(password);          // always run, so timing says nothing
  if (!okEmail || !okPass || !process.env.ADMIN_SESSION_SECRET) {
    t.n += 1;
    if (t.n >= 6) { t.n = 0; t.until = Date.now() + 15 * 60e3; }
    tries.set(ip, t);
    await new Promise(r => setTimeout(r, 600));
    return A.send(res, 401, { ok: false, error: 'That email or password is not right.' });
  }
  tries.delete(ip);
  A.send(res, 200, { ok: true, email: process.env.ADMIN_EMAIL },
    { 'Set-Cookie': A.cookie(A.makeSession(process.env.ADMIN_EMAIL), A.SESSION_HOURS * 3600) });
}

async function content(req, res) {
  if (req.method === 'GET') {
    if (!A.guard(req, res)) return;
    const path = String(req.query.path || '');
    if (!A.EDITABLE.test(path)) return A.send(res, 400, { ok: false, error: 'Not an editable file.' });
    const f = await A.readFile(path);
    return A.send(res, 200, { ok: true, sha: f.sha, data: JSON.parse(f.text) });
  }
  const s = A.guard(req, res, { write: true });
  if (!s) return;
  const body = await A.readJson(req);
  const path = String(body.path || '');
  if (!A.EDITABLE.test(path)) return A.send(res, 400, { ok: false, error: 'Not an editable file.' });
  if (req.method === 'PUT') {
    const data = A.validate(path, body.data);
    const msg = String(body.message || `Update ${path.split('/').pop()}`).replace(/\s+/g, ' ').slice(0, 120);
    const r = await A.writeFile(path, JSON.stringify(data, null, 2) + '\n', msg, body.sha || undefined, s.e);
    return A.send(res, 200, { ok: true, sha: r.content.sha, commit: r.commit.sha });
  }
  if (req.method === 'DELETE') {
    if (!/^content\/(journal\/posts|events)\//.test(path)) return A.send(res, 400, { ok: false, error: 'Only posts and events can be deleted.' });
    const r = await A.deleteFile(path, `Delete ${path.split('/').pop()}`, body.sha, s.e);
    return A.send(res, 200, { ok: true, commit: r.commit.sha });
  }
  A.send(res, 405, { ok: false });
}

async function events(req, res) {
  if (!A.guard(req, res)) return;
  let list = [];
  try { list = await A.gh(`/contents/content/events?ref=${A.BRANCH}&t=${Date.now()}`); } catch (e) { if (e.status !== 404) throw e; }
  const out = await Promise.all(list.filter(f => f.name.endsWith('.json')).map(async f => {
    const { text, sha } = await A.readFile(f.path);
    const e = JSON.parse(text);
    return { path: f.path, sha, slug: e.slug, date: e.date, time: e.time, draft: !!e.draft, featured: !!e.featured,
      title: (e.en || {}).title || e.slug, title_it: (e.it || {}).title || '', photo: (e.photo || {}).desk || '' };
  }));
  out.sort((a, b) => (b.date + b.time).localeCompare(a.date + a.time));
  A.send(res, 200, { ok: true, events: out });
}

async function leads(req, res) {
  if (req.method === 'GET') {
    if (!A.guard(req, res)) return;
    const j = await A.sheet({ action: 'leads' });
    return A.send(res, 200, { ok: true, leads: j.leads, statuses: j.statuses });
  }
  const s = A.guard(req, res, { write: true });
  if (!s) return;
  const { row, status } = await A.readJson(req, 10000);
  await A.sheet({ action: 'status', row, status });
  A.send(res, 200, { ok: true });
}

async function posts(req, res) {
  if (!A.guard(req, res)) return;
  let list = [];
  try { list = await A.gh(`/contents/content/journal/posts?ref=${A.BRANCH}&t=${Date.now()}`); } catch (e) { if (e.status !== 404) throw e; }
  const out = await Promise.all(list.filter(f => f.name.endsWith('.json')).map(async f => {
    const { text, sha } = await A.readFile(f.path);
    const p = JSON.parse(text);
    return { path: f.path, sha, slug: p.slug, date: p.date, draft: !!p.draft, category: p.category,
      title: (p.en || {}).title || p.slug, title_it: (p.it || {}).title || '', photo: (p.photo || {}).base || '' };
  }));
  out.sort((a, b) => (b.date || '').localeCompare(a.date || ''));
  A.send(res, 200, { ok: true, posts: out });
}

const TYPES = { 'image/jpeg': 'jpg', 'image/png': 'png', 'image/webp': 'webp' };

function sniff(buf) {
  if (buf[0] === 0xff && buf[1] === 0xd8) return 'image/jpeg';
  if (buf.slice(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]))) return 'image/png';
  if (buf.slice(0, 4).toString() === 'RIFF' && buf.slice(8, 12).toString() === 'WEBP') return 'image/webp';
  return null;
}

async function upload(req, res) {
  if (req.method !== 'POST') return A.send(res, 405, { ok: false });
  const s = A.guard(req, res, { write: true });
  if (!s) return;
  const { name, data } = await A.readJson(req, 30 * 1024 * 1024);
  const buf = Buffer.from(String(data || ''), 'base64');
  const type = sniff(buf);
  if (!type) return A.send(res, 400, { ok: false, error: 'Please upload a JPEG, PNG or WebP photo.' });
  if (buf.length > 15 * 1024 * 1024) return A.send(res, 400, { ok: false, error: 'That photo is over 15 MB.' });
  const slug = String(name || 'photo').replace(/\.[^.]+$/, '').normalize('NFKD').replace(/[\u0300-\u036f]/g, '')
    .toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 50) || 'photo';
  const d = new Date();
  const dir = `${d.getUTCFullYear()}/${String(d.getUTCMonth() + 1).padStart(2, '0')}`;
  const file = `${slug}-${crypto.randomBytes(3).toString('hex')}`;
  await A.writeFile(`content/uploads/${dir}/${file}.${TYPES[type]}`, buf, `Upload photo ${file}`, undefined, s.e);
  A.send(res, 200, { ok: true, base: `/wp-content/uploads/${dir}/${file}` });
}

async function status(req, res) {
  if (!A.guard(req, res)) return;
  const [runs, commits] = await Promise.all([
    A.gh(`/actions/workflows/publish-content.yml/runs?branch=${A.BRANCH}&per_page=3`).catch(() => ({ workflow_runs: [] })),
    A.gh(`/commits?sha=${A.BRANCH}&per_page=1`),
  ]);
  const head = commits[0];
  const run = (runs.workflow_runs || [])[0];
  let deploy = null;
  try {
    const st = await A.gh(`/commits/${head.sha}/status`);
    const v = (st.statuses || []).find(x => /vercel/i.test(x.context || ''));
    deploy = v ? v.state : null;                     // pending | success | failure | error
  } catch (e) { /* no status yet */ }
  let state = 'live';
  if (run && ['queued', 'in_progress', 'waiting', 'requested', 'pending'].includes(run.status)) state = 'publishing';
  else if (run && run.conclusion === 'failure') state = 'failed';
  else if (deploy === 'pending') state = 'publishing';
  else if (deploy === 'failure' || deploy === 'error') state = 'failed';
  A.send(res, 200, { ok: true, state, head: { sha: head.sha.slice(0, 7), message: head.commit.message.split('\n')[0], date: head.commit.committer.date },
    run: run ? { status: run.status, conclusion: run.conclusion, url: run.html_url, head_sha: run.head_sha } : null, deploy });
}

module.exports = async (req, res) => {
  const action = String((req.query && req.query.action) || '').toLowerCase();
  try {
    if (action === 'login') return await login(req, res);
    if (action === 'logout') return A.send(res, 200, { ok: true }, { 'Set-Cookie': A.cookie('', 0) });
    if (action === 'me') {
      const s = A.readSession(req);
      return A.send(res, s ? 200 : 401, s ? { ok: true, email: s.e, github: !!process.env.GITHUB_TOKEN, leads: !!process.env.LEADS_KEY } : { ok: false });
    }
    if (action === 'content') return await content(req, res);
    if (action === 'posts') return await posts(req, res);
    if (action === 'events') return await events(req, res);
    if (action === 'leads') return await leads(req, res);
    if (action === 'upload') return await upload(req, res);
    if (action === 'status') return await status(req, res);
    A.send(res, 404, { ok: false });
  } catch (e) {
    const code = e.status === 409 || e.status === 422 ? 409 : (e.status >= 400 && e.status < 600 ? e.status : 500);
    A.send(res, code, { ok: false, error: code === 409
      ? 'This was changed somewhere else since you opened it. Reload to get the latest, then make your change again.'
      : (code === 500 ? 'Something went wrong while saving. Nothing was changed.' : e.message) });
    if (code === 500) console.error('[admin]', action, e);
  }
};
