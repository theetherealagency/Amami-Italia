// Shared helpers for the admin portal API (/api/admin/*).
//
// Sign-in: one account. ADMIN_EMAIL and ADMIN_PASSWORD_HASH (scrypt, made by
// tools/admin-password.js) are Vercel environment variables; the password
// itself is never stored. A signed, HttpOnly cookie keeps the client signed in
// for 12 hours.
//
// Saving: every change is committed to GitHub (GITHUB_TOKEN, a token that can
// write this one repository). The "Publish content" GitHub Action then builds
// the pages and Vercel deploys them, about a minute end to end.
const crypto = require('crypto');

const REPO = process.env.GITHUB_REPO || 'theetherealagency/Amami-Italia';
const BRANCH = process.env.GITHUB_BRANCH || 'main';
const COOKIE = 'amami_admin';
const SESSION_HOURS = 12;

function send(res, status, body, headers = {}) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('X-Robots-Tag', 'noindex');
  for (const [k, v] of Object.entries(headers)) res.setHeader(k, v);
  res.end(JSON.stringify(body));
}

async function readJson(req, limit = 20 * 1024 * 1024) {
  if (req.body && typeof req.body === 'object' && !Buffer.isBuffer(req.body)) return req.body;
  let raw = typeof req.body === 'string' ? req.body : Buffer.isBuffer(req.body) ? req.body.toString('utf8') : '';
  if (!raw) {
    raw = await new Promise((resolve, reject) => {
      let s = '', n = 0;
      req.on('data', c => { n += c.length; if (n > limit) { reject(new Error('too large')); req.destroy(); } else s += c; });
      req.on('end', () => resolve(s));
      req.on('error', reject);
    });
  }
  return raw ? JSON.parse(raw) : {};
}

// ---- password + session ------------------------------------------------------

function checkPassword(password) {
  const stored = process.env.ADMIN_PASSWORD_HASH || '';
  const [alg, N, r, p, salt, hash] = stored.split('$');
  if (alg !== 'scrypt' || !hash) return false;
  const want = Buffer.from(hash, 'base64');
  const got = crypto.scryptSync(String(password || ''), Buffer.from(salt, 'base64'), want.length,
    { N: +N, r: +r, p: +p, maxmem: 256 * 1024 * 1024 });
  return crypto.timingSafeEqual(want, got);
}

function sessionKey() {
  // bound to the password hash: changing the password signs everyone out
  return crypto.createHash('sha256')
    .update(String(process.env.ADMIN_SESSION_SECRET || '') + '|' + String(process.env.ADMIN_PASSWORD_HASH || ''))
    .digest();
}

function b64url(buf) { return Buffer.from(buf).toString('base64url'); }

function makeSession(email) {
  const payload = b64url(JSON.stringify({ e: email, x: Date.now() + SESSION_HOURS * 3600e3 }));
  const sig = b64url(crypto.createHmac('sha256', sessionKey()).update(payload).digest());
  return `${payload}.${sig}`;
}

function readSession(req) {
  const m = /(?:^|;\s*)amami_admin=([^;]+)/.exec(req.headers.cookie || '');
  if (!m || !process.env.ADMIN_SESSION_SECRET) return null;
  const [payload, sig] = m[1].split('.');
  if (!payload || !sig) return null;
  const want = crypto.createHmac('sha256', sessionKey()).update(payload).digest();
  const got = Buffer.from(sig, 'base64url');
  if (got.length !== want.length || !crypto.timingSafeEqual(got, want)) return null;
  try {
    const s = JSON.parse(Buffer.from(payload, 'base64url').toString('utf8'));
    return s.x > Date.now() ? s : null;
  } catch (e) { return null; }
}

function cookie(value, maxAge) {
  return `${COOKIE}=${value}; Path=/api/admin; HttpOnly; Secure; SameSite=Strict; Max-Age=${maxAge}`;
}

// Writes need the session cookie plus a header a cross-site form cannot send.
function guard(req, res, { write = false } = {}) {
  const s = readSession(req);
  if (!s) { send(res, 401, { ok: false, error: 'signed-out' }); return null; }
  if (write) {
    const origin = req.headers.origin;
    if (req.headers['x-amami-admin'] !== '1' || (origin && new URL(origin).host !== req.headers.host)) {
      send(res, 403, { ok: false, error: 'forbidden' }); return null;
    }
  }
  return s;
}

// ---- GitHub ------------------------------------------------------------------

async function gh(path, opts = {}) {
  if (!process.env.GITHUB_TOKEN) {
    const e = new Error('The portal is not connected to GitHub yet (GITHUB_TOKEN is missing).');
    e.status = 503; throw e;
  }
  const r = await fetch(`https://api.github.com/repos/${REPO}${path}`, {
    ...opts,
    headers: {
      Authorization: `Bearer ${process.env.GITHUB_TOKEN}`,
      Accept: 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
      'User-Agent': 'amami-admin-portal',
      ...(opts.body ? { 'Content-Type': 'application/json' } : {}),
    },
  });
  const text = await r.text();
  const body = text ? JSON.parse(text) : {};
  if (!r.ok) {
    const e = new Error(body.message || `GitHub ${r.status}`);
    e.status = r.status; throw e;
  }
  return body;
}

async function readFile(path) {
  const f = await gh(`/contents/${encodeURI(path)}?ref=${BRANCH}&t=${Date.now()}`);
  return { text: Buffer.from(f.content, 'base64').toString('utf8'), sha: f.sha };
}

function author(email) {
  return { name: 'Amami Italia (admin portal)', email: email || process.env.ADMIN_EMAIL || 'admin@amamiitalia.com' };
}

async function writeFile(path, contentBuf, message, sha, email) {
  return gh(`/contents/${encodeURI(path)}`, {
    method: 'PUT',
    body: JSON.stringify({ message, content: Buffer.from(contentBuf).toString('base64'), branch: BRANCH,
      ...(sha ? { sha } : {}), author: author(email), committer: author(email) }),
  });
}

async function deleteFile(path, message, sha, email) {
  return gh(`/contents/${encodeURI(path)}`, {
    method: 'DELETE',
    body: JSON.stringify({ message, sha, branch: BRANCH, author: author(email), committer: author(email) }),
  });
}

// ---- content rules -------------------------------------------------------------

const EDITABLE = /^content\/(site\/(events|menu)\.json|journal\/categories\.json|(journal\/posts|events)\/[a-z0-9]+(?:-[a-z0-9]+)*\.json)$/;

// Writing tags and the Journal's own classes; everything else is dropped.
const TAGS = new Set(['p', 'h2', 'h3', 'h4', 'strong', 'b', 'em', 'i', 'a', 'br', 'ul', 'ol', 'li', 'blockquote', 'span',
  'div', 'aside', 'section', 'figure', 'figcaption', 'table', 'caption', 'thead', 'tbody', 'tr', 'th', 'td', 'abbr',
  'sup', 'sub', 'hr', 'cite', 'small', 'img']);
const ATTRS = new Set(['href', 'class', 'title', 'src', 'alt', 'width', 'height', 'loading', 'rel', 'target', 'colspan', 'rowspan', 'scope']);

function cleanHtml(s) {
  s = String(s || '').replace(/<(script|style|iframe|object|embed|form|template|noscript)\b[\s\S]*?<\/\1\s*>/gi, '')
    .replace(/<!--[\s\S]*?-->/g, '');
  return s.replace(/<\/?([a-zA-Z0-9]+)\b([^>]*)>/g, (m, tag, attrs) => {
    tag = tag.toLowerCase();
    if (!TAGS.has(tag)) return '';
    if (m.startsWith('</')) return `</${tag}>`;
    const kept = [];
    attrs.replace(/([a-zA-Z-]+)\s*=\s*("([^"]*)"|'([^']*)')/g, (_, name, __, dq, sq) => {
      name = name.toLowerCase();
      let v = dq !== undefined ? dq : sq;
      if (!ATTRS.has(name)) return;
      if ((name === 'href' || name === 'src') && /^\s*(javascript|data|vbscript):/i.test(v)) return;
      kept.push(`${name}="${v.replace(/"/g, '&quot;')}"`);
    });
    return `<${tag}${kept.length ? ' ' + kept.join(' ') : ''}>`;
  });
}

function textOk(v, max = 5000) { return typeof v === 'string' && v.length <= max; }

// Light checks so a mistake in the portal can never break the build.
function validate(path, data) {
  if (!data || typeof data !== 'object') throw bad('The content is empty.');
  if (/journal\/posts\//.test(path)) {
    const slug = path.split('/').pop().replace(/\.json$/, '');
    if (data.slug !== slug) throw bad('The post address does not match its file.');
    if (!/^\d{4}-\d\d-\d\d$/.test(data.date || '')) throw bad('The post needs a date.');
    if (!data.draft && (!data.photo || !/^\/wp-content\/uploads\/[\w/.-]+$/.test(data.photo.base || ''))) throw bad('Add a banner photo before publishing.');
    for (const lang of ['en', 'it']) {
      const L = data[lang];
      if (!L || !textOk(L.title, 200) || !L.title.trim()) throw bad(`The ${lang === 'en' ? 'English' : 'Italian'} title is missing.`);
      L.body_html = cleanHtml(L.body_html);
      if (typeof L.dek === 'string') L.dek = L.dek.replace(/<[^>]*>/g, '');
      for (const k of Object.keys(L)) if (typeof L[k] === 'string' && k !== 'body_html' && L[k].length > 2000) throw bad(`"${k}" is too long.`);
    }
  }
  if (/^content\/events\//.test(path)) {
    const slug = path.split('/').pop().replace(/\.json$/, '');
    if (data.slug !== slug) throw bad('The event address does not match its file.');
    if (!/^\d{4}-\d\d-\d\d$/.test(data.date || '')) throw bad('The event needs a date.');
    if (!/^\d\d:\d\d$/.test(data.time || '')) throw bad('The event needs a time.');
    if (!data.draft && !/^\/wp-content\/uploads\/[\w/.-]+$/.test((data.photo || {}).desk || '')) throw bad('Add a photo before publishing the event.');
    for (const lang of ['en', 'it']) {
      const L = data[lang];
      if (!L || !textOk(L.title, 160) || !L.title.trim()) throw bad(`The ${lang === 'en' ? 'English' : 'Italian'} event name is missing.`);
      for (const k of ['intro_html', 'after_html']) if (typeof L[k] === 'string') L[k] = cleanHtml(L[k]);
      for (const k of Object.keys(L)) if (typeof L[k] === 'string' && !/_html$/.test(k) && L[k].length > 2000) throw bad(`"${k}" is too long.`);
    }
  }
  if (/site\/events\.json$/.test(path)) {
    if (!data.slots || typeof data.slots !== 'object') throw bad('The Events page content is empty.');
  }
  if (/site\/menu\.json$/.test(path)) {
    for (const [page, m] of Object.entries(data.menus || {})) {
      for (const sec of m.sections || []) {
        for (const it of sec.items || []) {
          if (!textOk(it.name, 160) || !it.name.trim()) throw bad(`A dish on the ${page} menu has no name.`);
          if (!textOk(it.price || '', 40)) throw bad(`The price of ${it.name} is too long.`);
        }
      }
    }
  }
  return data;
}

function bad(msg) { const e = new Error(msg); e.status = 400; return e; }

// The Google Sheet behind the event enquiry form (apps-script/enquiries.gs).
const SCRIPT_URL = process.env.FORMS_SCRIPT_URL ||
  'https://script.google.com/macros/s/AKfycbwvrH3PsAW6LZQ1D2SBX9RwgX4_qM29xvE0QlWc77wFSpb7ghJyHHV_GUwwXOO9WUHwjA/exec';

async function sheet(body) {
  if (!process.env.LEADS_KEY) { const e = new Error('Leads are not connected yet (LEADS_KEY is missing).'); e.status = 503; throw e; }
  const r = await fetch(SCRIPT_URL, { method: 'POST', redirect: 'follow', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...body, key: process.env.LEADS_KEY }) });
  const text = await r.text();
  let j;
  try { j = JSON.parse(text); } catch (e) { const x = new Error('The enquiry sheet did not answer. Try again in a minute.'); x.status = 502; throw x; }
  if (!j.ok) {
    const old = j.error === 'not allowed' || /email address is required|Only event enquiries/i.test(j.error || '');
    const x = new Error(old
      ? 'The enquiry sheet has not been updated for the portal yet (paste the new Code.gs and deploy a new version).'
      : (j.error || 'The enquiry sheet returned an error.'));
    x.status = 502; throw x;
  }
  return j;
}

module.exports = { sheet, send, readJson, checkPassword, makeSession, readSession, cookie, guard, gh, readFile, writeFile,
  deleteFile, EDITABLE, validate, cleanHtml, REPO, BRANCH, SESSION_HOURS };
