/* Amami Italia admin portal (/admin/).
   Edits the JSON under content/ through /api/admin/*; saving commits to GitHub and
   the "Publish content" action rebuilds the pages. No framework, no build step. */
(() => {
'use strict';

// ---------- small helpers ----------
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const clone = o => JSON.parse(JSON.stringify(o));
const today = () => new Date().toLocaleDateString('en-CA');
const getIn = (o, p) => p.reduce((a, k) => (a == null ? a : a[k]), o);
function setIn(o, p, v) { let a = o; for (let i = 0; i < p.length - 1; i++) { if (a[p[i]] == null) a[p[i]] = typeof p[i + 1] === 'number' ? [] : {}; a = a[p[i]]; } a[p[p.length - 1]] = v; }
const P = p => esc(JSON.stringify(p));
const slugify = s => String(s || '').normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
  .replace(/&/g, ' and ').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 70).replace(/-+$/, '');

const ICONS = {
  grid: '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
  ticket: '<path d="M3 9a3 3 0 0 0 0 6v2a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-2a3 3 0 0 0 0-6V7a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2z"/><path d="M13 5v2M13 17v2M13 11v2"/>',
  book: '<path d="M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2z"/><path d="M22 4h-6a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h7z"/>',
  menu: '<path d="M3 2v7c0 1.1.9 2 2 2h2a2 2 0 0 0 2-2V2M6 2v20M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3zm0 0v7"/>',
  image: '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.1-3.1a2 2 0 0 0-2.8 0L6 21"/>',
  ext: '<path d="M15 3h6v6M10 14 21 3M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
  out: '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/>',
  warn: '<path d="m21.7 18-8-14a2 2 0 0 0-3.4 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.7-3M12 9v4M12 17h.01"/>',
  ok: '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
  load: '<path d="M21 12a9 9 0 1 1-6.2-8.6"/>',
  plus: '<path d="M12 5v14M5 12h14"/>',
  trash: '<path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>',
  up: '<path d="m18 15-6-6-6 6"/>', down: '<path d="m6 9 6 6 6-6"/>',
  arrow: '<path d="M5 12h14M12 5l7 7-7 7"/>', upload: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/>',
  inbox: '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>',
  bars: '<path d="M4 6h16M4 12h16M4 18h16"/>', search: '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
};
const ic = (n, cls = '') => `<svg class="i ${cls}" viewBox="0 0 24 24" aria-hidden="true">${ICONS[n]}</svg>`;

function toast(msg, bad = false) {
  let box = $('.toast');
  if (!box) { box = document.createElement('div'); box.className = 'toast'; document.body.appendChild(box); }
  const d = document.createElement('div');
  if (bad) d.className = 't--bad';
  d.textContent = msg;
  box.appendChild(d);
  setTimeout(() => d.remove(), bad ? 7000 : 3800);
}

// ---------- API ----------
async function api(action, { method = 'GET', query, body } = {}) {
  const url = `/api/admin/${action}/` + (query ? '?' + new URLSearchParams(query) : '');
  const headers = method === 'GET' ? {} : { 'X-Amami-Admin': '1', 'Content-Type': 'application/json' };
  const r = await fetch(url, { method, credentials: 'same-origin', headers, body: body ? JSON.stringify(body) : undefined });
  let j = {};
  try { j = await r.json(); } catch (e) { /* empty */ }
  if (r.status === 401 && !['login', 'me'].includes(action)) { S.me = null; render(); throw new Error('Your session ended. Please sign in again.'); }
  if (!r.ok || j.ok === false) throw Object.assign(new Error(j.error || `Something went wrong (${r.status}).`), { status: r.status });
  return j;
}

// ---------- state ----------
const EVENTS = 'content/site/events.json', MENU = 'content/site/menu.json', CATS = 'content/journal/categories.json';
const S = { me: null, files: {}, posts: null, previews: {}, status: null, pending: null, view: null, busy: false };

async function load(path, force) {
  if (force || !S.files[path]) {
    const j = await api('content', { query: { path } });
    S.files[path] = { data: j.data, sha: j.sha, orig: JSON.stringify(j.data) };
  }
  return S.files[path];
}
const dirty = path => { const f = S.files[path]; return !!f && JSON.stringify(f.data) !== f.orig; };
const anyDirty = () => Object.keys(S.files).some(dirty);

async function save(key, message, path = key) {
  const f = S.files[key];
  const j = await api('content', { method: 'PUT', body: { path, data: f.data, sha: f.sha, message } });
  f.sha = j.sha; f.orig = JSON.stringify(f.data);
  S.pending = { commit: j.commit, since: Date.now() };
  watchStatus();
  return j;
}

// ---------- publishing status ----------
let statusTimer = null;
async function refreshStatus() {
  try {
    const s = await api('status');
    if (S.pending) {
      const p = S.pending;
      const done = s.run && s.run.head_sha === p.commit && s.run.status === 'completed' && s.deploy !== 'pending';
      if (done) { S.pending = null; if (s.state === 'live') toast('Your changes are live on the website.'); }
      else if (Date.now() - p.since > 6 * 60e3) S.pending = null;
      else s.state = s.state === 'failed' && s.run && s.run.head_sha === p.commit ? 'failed' : 'publishing';
    }
    S.status = s;
  } catch (e) { S.status = S.status || null; }
  paintStatus();
  clearTimeout(statusTimer);
  if (S.pending || (S.status && S.status.state === 'publishing')) statusTimer = setTimeout(refreshStatus, 4000);
}
function watchStatus() { S.status = Object.assign({}, S.status || {}, { state: 'publishing' }); paintStatus(); clearTimeout(statusTimer); statusTimer = setTimeout(refreshStatus, 3000); }
function statusBadge() {
  const st = S.status && S.status.state;
  if (st === 'publishing') return `<span class="badge badge--warn">${ic('load', 'spin')} Publishing…</span>`;
  if (st === 'failed') return `<span class="badge badge--bad"><span class="dot"></span> Last publish failed</span>`;
  if (st === 'live') return `<span class="badge badge--ok"><span class="dot"></span> Website up to date</span>`;
  return `<span class="badge">Checking…</span>`;
}
function paintStatus() { $$('[data-status]').forEach(el => { el.innerHTML = statusBadge(); }); }

// ---------- photos ----------
function thumbs(base) {
  if (!base) return [];
  if (S.previews[base]) return [S.previews[base]];
  return ['-800w.jpg', '-800w.webp', '-1200w.jpg', '-1200w.webp', '-480w.webp', '-1100w.webp', '.jpg', '.webp'].map(x => base + x);
}
function imgTag(base, alt = '') {
  const t = thumbs(base);
  if (!t.length) return `<div class="ph__img">No photo yet</div>`;
  return `<div class="ph__img"><img src="${esc(t[0])}" data-alts="${esc(t.slice(1).join('|'))}" alt="${esc(alt)}" style="width:100%;height:100%;object-fit:cover" loading="lazy"></div>`;
}
document.addEventListener('error', e => {
  const im = e.target;
  if (im.tagName !== 'IMG' || !im.dataset.alts) return;
  const rest = im.dataset.alts.split('|').filter(Boolean);
  if (!rest.length) { im.replaceWith(Object.assign(document.createElement('span'), { textContent: 'Preview not available' })); return; }
  im.dataset.alts = rest.slice(1).join('|');
  im.src = rest[0];
}, true);

async function prepareImage(file) {
  if (!/^image\/(jpeg|png|webp|heic|heif)$/i.test(file.type) && !/\.(jpe?g|png|webp)$/i.test(file.name)) throw new Error('Please choose a JPEG, PNG or WebP photo.');
  const bmp = await createImageBitmap(file, { imageOrientation: 'from-image' }).catch(() => { throw new Error('That photo could not be opened. Try saving it as a JPEG first.'); });
  let w = bmp.width, h = bmp.height;
  if (w < 600) throw new Error('That photo is too small for the website (at least 600 px wide, please).');
  if (w > 2400) { h = Math.round(h * 2400 / w); w = 2400; }
  const c = document.createElement('canvas');
  c.width = w; c.height = h;
  c.getContext('2d').drawImage(bmp, 0, 0, w, h);
  const blob = await new Promise(r => c.toBlob(r, 'image/jpeg', 0.92));
  const data = await new Promise(r => { const fr = new FileReader(); fr.onload = () => r(String(fr.result).split(',')[1]); fr.readAsDataURL(blob); });
  return { data, w, h, preview: URL.createObjectURL(blob) };
}

// target: {f: file path, p: path to the object, role: 'desk' | 'mob' | 'post'}
async function uploadInto(target, file) {
  toast('Uploading photo…');
  const img = await prepareImage(file);
  const j = await api('upload', { method: 'POST', body: { name: file.name, data: img.data } });
  S.previews[j.base] = img.preview;
  const obj = getIn(S.files[target.f].data, target.p) || {};
  if (target.role === 'post') { obj.base = j.base; obj.width = img.w; obj.height = img.h; }
  else { obj[target.role] = j.base; if (target.role === 'desk' && obj.w) { obj.w = img.w; obj.h = img.h; } }
  setIn(S.files[target.f].data, target.p, obj);
  render();
  toast('Photo uploaded. Press Save to put it on the website.');
}

// ---------- fields ----------
const L = { en: 'EN', it: 'IT' };
function input(f, p, { type = 'text', ph = '', max, rows, cls = '' } = {}) {
  const v = getIn(S.files[f].data, p) ?? '';
  const attrs = `class="in ${cls}" data-f="${esc(f)}" data-p="${P(p)}" placeholder="${esc(ph)}"${max ? ` data-max="${max}"` : ''}`;
  if (rows) return `<textarea ${attrs} rows="${rows}">${esc(v)}</textarea>`;
  return `<input ${attrs} type="${type}" value="${esc(v)}">`;
}
function field(label, f, p, opts = {}) {
  return `<label class="f"><span class="f__l">${esc(label)}${opts.note ? `<small>${esc(opts.note)}</small>` : ''}</span>${input(f, p, opts)}</label>`;
}
// English and Italian side by side
function pair(label, f, p, opts = {}) {
  return `<div class="f"><span class="f__l">${esc(label)}${opts.note ? `<small>${esc(opts.note)}</small>` : ''}</span><div class="pair">
    <label><span class="lang">EN</span>${input(f, [...p, 'en'], opts)}</label>
    <label><span class="lang">IT</span>${input(f, [...p, 'it'], opts)}</label></div></div>`;
}
function check(label, f, p) {
  const v = !!getIn(S.files[f].data, p);
  return `<label class="check"><input type="checkbox" data-f="${esc(f)}" data-p="${P(p)}" ${v ? 'checked' : ''}> ${esc(label)}</label>`;
}
function photoCard(label, f, p, role, alt) {
  const obj = getIn(S.files[f].data, p) || {};
  const base = role === 'post' ? obj.base : obj[role];
  const fresh = base && S.previews[base];
  return `<div class="ph">${imgTag(base, alt)}<div class="ph__b"><div><b>${esc(label)}</b>${fresh ? '<div class="ph__new">New, not saved yet</div>' : ''}</div>
    <button class="btn btn--sm" type="button" data-upload='${esc(JSON.stringify({ f, p, role }))}'>${ic('upload')} Replace</button></div></div>`;
}
function imageField(label, f, key, { mob } = {}) {
  const p = ['slots', key];
  const v = getIn(S.files[f].data, p) || {};
  return `<div class="f"><span class="f__l">${esc(label)}<small>Photos are resized for phones and computers automatically. No filters are added.</small></span>
    <div class="imgfield">${photoCard(mob === false || !v.mob ? 'Photo' : 'Computer', f, p, 'desk', (v.alt || {}).en)}${v.mob ? photoCard('Phone', f, p, 'mob', (v.alt || {}).en) : ''}</div>
    ${pair('Describe the photo', f, [...p, 'alt'], { note: 'For Google and for people using screen readers' })}</div>`;
}

document.addEventListener('input', e => {
  const el = e.target;
  if (!el.dataset || !el.dataset.f || !el.dataset.p) return;
  const f = S.files[el.dataset.f];
  if (!f) return;
  const p = JSON.parse(el.dataset.p);
  setIn(f.data, p, el.type === 'checkbox' ? el.checked : el.value);
  if (el.dataset.max) el.classList.toggle('in--bad', el.value.length > +el.dataset.max);
  if (S.view && S.view.onInput) S.view.onInput(el, p);
  paintSaveBar();
});
document.addEventListener('change', e => { if (e.target.type === 'checkbox') e.target.dispatchEvent(new Event('input', { bubbles: true })); });
document.addEventListener('click', e => {
  const up = e.target.closest('[data-upload]');
  if (up) {
    const target = JSON.parse(up.dataset.upload);
    const pick = Object.assign(document.createElement('input'), { type: 'file', accept: 'image/jpeg,image/png,image/webp' });
    pick.onchange = () => pick.files[0] && uploadInto(target, pick.files[0]).catch(err => toast(err.message, true));
    pick.click();
  }
  const nav = e.target.closest('[data-toggle-nav]');
  if (nav) $('.shell').classList.toggle('nav-open');
  if (e.target.closest('.nav a')) { const sh = $('.shell'); if (sh) sh.classList.remove('nav-open'); }
});
window.addEventListener('beforeunload', e => { if (anyDirty()) { e.preventDefault(); e.returnValue = ''; } });

// ---------- save bar ----------
function paintSaveBar() {
  const bar = $('.savebar');
  if (!bar || !S.view) return;
  const on = (S.view.files || []).some(dirty);
  bar.classList.toggle('is-on', on);
}
async function saveView() {
  if (S.busy) return;
  const v = S.view;
  const errs = v.check ? v.check() : [];
  if (errs.length) { toast(errs[0], true); return; }
  S.busy = true;
  $$('.savebar button').forEach(b => { b.disabled = true; });
  try {
    for (const f of v.files) if (dirty(f)) await save(f, v.message ? v.message(f) : `Update ${v.title}`, v.pathFor ? v.pathFor(f) : f);
    toast('Saved. Publishing to the website, about a minute…');
    if (v.after) await v.after();
    render();
  } catch (err) {
    toast(err.message, true);
  } finally {
    S.busy = false;
    $$('.savebar button').forEach(b => { b.disabled = false; });
    paintSaveBar();
  }
}
function discardView() {
  for (const f of S.view.files || []) if (S.files[f]) S.files[f].data = JSON.parse(S.files[f].orig);
  render();
}

// ---------- shell ----------
const NAV = [['dashboard', 'Dashboard', 'grid'], ['leads', 'Leads', 'inbox'], ['events', 'Events', 'ticket'], ['journal', 'Journal', 'book'], ['menu', 'Menu', 'menu'], ['photos', 'Photos', 'image']];
function shell(route, body) {
  return `<div class="shell">
  <aside class="side">
    <div class="side__who"><b>Amami Italia Admin</b><span>${esc(S.me.email)}</span></div>
    <nav class="nav">${NAV.map(([r, t, i]) => `<a href="#/${r}" ${route === r ? 'aria-current="page"' : ''}>${ic(i)} ${t}</a>`).join('')}</nav>
    <div class="side__foot nav">
      <a href="/" target="_blank" rel="noopener">${ic('ext')} View website</a>
      <a href="#/signout">${ic('out')} Sign out</a>
    </div>
  </aside>
  <div>
    <div class="topbar"><button class="btn btn--icon btn--ghost" data-toggle-nav aria-label="Menu">${ic('bars')}</button><b>Amami Italia Admin</b></div>
    <main class="main">${body}</main>
  </div>
  <div class="savebar"><span><b>You have unsaved changes.</b> <span class="muted">Nothing changes on the website until you save.</span></span>
    <span class="btns"><button class="btn" type="button" id="discard">Discard</button><button class="btn btn--dark" type="button" id="save">Save and publish</button></span></div>
</div>`;
}
function head(title, sub, right = '') {
  return `<div style="display:flex;justify-content:space-between;gap:16px;align-items:flex-start;flex-wrap:wrap"><div><h1 class="h1">${esc(title)}</h1><p class="sub">${esc(sub)}</p></div><div class="btns">${right}<span data-status>${statusBadge()}</span></div></div>`;
}

// ---------- sign in ----------
function loginView() {
  document.title = 'Sign in | Amami Italia Admin';
  $('#app').innerHTML = `<div class="login"><form class="login__card" id="login">
    <h1>Amami Italia Admin</h1><p>Sign in to update the website.</p>
    <label class="f"><span class="f__l">Email</span><input class="in" name="email" type="email" autocomplete="username" required autofocus></label>
    <label class="f"><span class="f__l">Password</span><input class="in" name="password" type="password" autocomplete="current-password" required></label>
    <p class="muted" id="login-err" role="alert" style="color:var(--bad);min-height:1.2em;margin:0 0 10px"></p>
    <button class="btn btn--dark" style="width:100%" type="submit">Sign in</button></form></div>`;
  $('#login').addEventListener('submit', async e => {
    e.preventDefault();
    const fd = new FormData(e.target), btn = $('button', e.target);
    btn.disabled = true; $('#login-err').textContent = '';
    try {
      await api('login', { method: 'POST', body: { email: fd.get('email'), password: fd.get('password') } });
      const me = await api('me');
      S.me = me;
      if (!location.hash || location.hash === '#/signout') location.hash = '#/dashboard';
      render(); refreshStatus();
    } catch (err) { $('#login-err').textContent = err.message; btn.disabled = false; }
  });
}

// ---------- dashboard ----------
async function dashboard() {
  const [ev, mn] = await Promise.all([load(EVENTS), load(MENU)]);
  if (!S.posts) S.posts = (await api('posts')).posts;
  if (!S.events) S.events = (await api('events')).events;
  let leadList = null;
  if (S.me.leads) { try { leadList = await loadLeads(); } catch (e) { leadList = null; } }
  const menus = mn.data.menus || {};
  const dishes = Object.values(menus).flatMap(m => m.sections.flatMap(s => s.items));
  const published = S.posts.filter(p => !p.draft), drafts = S.posts.filter(p => p.draft);
  const photos = Object.values(ev.data.slots).concat(Object.values(mn.data.slots)).filter(v => v && v.desk !== undefined).length;
  const up = S.events.filter(e => !e.draft && !isPast(e)).sort((a, b) => (a.date + a.time).localeCompare(b.date + b.time));
  const next = up.find(e => e.featured) || up[0];
  const newLeads = leadList ? leadList.filter(l => l.status === 'New') : [];
  const needs = [];
  if (!S.me.github) needs.push(['The portal is not connected to GitHub yet, so saving is switched off.', '#/dashboard', 'bad']);
  if (newLeads.length) needs.push([`${newLeads.length} new event enquir${newLeads.length > 1 ? 'ies' : 'y'} to answer.`, '#/leads']);
  if (S.me.leads && !leadList) needs.push(['The enquiry sheet is not answering the portal yet. Leads will show here once it is updated.', '#/leads', 'bad']);
  if (!up.length) needs.push(['No event is coming up, so the event panel is hidden on the Events page. Add one.', '#/events/new']);
  const noIt = dishes.filter(d => d.desc && d.desc.en && !d.desc.it).length;
  if (noIt) needs.push([`${noIt} dish${noIt > 1 ? 'es have' : ' has'} no Italian description.`, '#/menu']);
  const evDrafts = S.events.filter(e => e.draft).length;
  if (evDrafts) needs.push([`${evDrafts} event${evDrafts > 1 ? 's are' : ' is'} saved as a draft and not on the website yet.`, '#/events']);
  if (drafts.length) needs.push([`${drafts.length} Journal post${drafts.length > 1 ? 's are' : ' is'} saved as a draft and not on the website yet.`, '#/journal']);
  const leadRow = l => `<a class="row" href="#/leads/${encodeURIComponent(l.space || 'Not sure yet')}"><span><span class="badge">${esc(l.space || 'Not sure yet')}</span> ${l.status === 'New' ? '<span class="badge badge--dark">New</span>' : ''}<br><b>${esc([l.firstName, l.lastName].filter(Boolean).join(' ') || l.email)}</b> <small class="muted">${esc(l.email)}</small></span><small>${esc(l.received ? new Date(l.received).toLocaleDateString('en-CA') : '')}</small></a>`;
  const body = head('Dashboard', "An overview of what's happening on the website.") + `
  <div class="stats">
    <a class="stat" href="#/leads"><span class="stat__i">${ic('inbox')}</span><div><b>${leadList ? newLeads.length : '–'}</b><span>New leads</span></div></a>
    <a class="stat" href="#/menu"><span class="stat__i">${ic('menu')}</span><div><b>${dishes.length}</b><span>Menu items</span></div></a>
    <a class="stat" href="#/events"><span class="stat__i">${ic('ticket')}</span><div><b>${up.length}</b><span>Upcoming events</span></div></a>
    <a class="stat" href="#/journal"><span class="stat__i">${ic('book')}</span><div><b>${published.length}</b><span>Journal posts${drafts.length ? ` · ${drafts.length} draft` : ''}</span></div></a>
    <a class="stat" href="#/photos"><span class="stat__i">${ic('image')}</span><div><b>${photos}</b><span>Page photos</span></div></a>
  </div>
  <div class="card"><h2>${ic(needs.length ? 'warn' : 'ok')} ${needs.length ? 'Needs attention' : 'All good'}</h2>
    <p class="hint">${needs.length ? `${needs.length} thing${needs.length > 1 ? 's' : ''} worth a look.` : 'Nothing needs your attention right now.'}</p>
    <div class="rows">${needs.map(([t, h, k]) => `<a class="row" href="${h}"><span${k === 'bad' ? ' style="color:var(--bad)"' : ''}>${esc(t)}</span>${ic('arrow')}</a>`).join('')}</div></div>
  <div class="card"><div style="display:flex;justify-content:space-between;gap:12px"><div><h2>Recent leads</h2><p class="hint">The latest event enquiries.</p></div><a class="btn" href="#/leads" style="align-self:flex-start">View all</a></div>
    <div class="rows">${leadList ? (leadList.slice(0, 5).map(leadRow).join('') || '<p class="muted">No enquiries yet.</p>') : '<p class="muted">Leads appear here once the enquiry sheet is connected.</p>'}</div></div>
  <div class="card"><div style="display:flex;justify-content:space-between;gap:12px"><div><h2>Coming up</h2><p class="hint">Upcoming events, soonest first.</p></div><a class="btn" href="#/events/new" style="align-self:flex-start">${ic('plus')} New event</a></div>
    <div class="rows">${up.map(e => `<a class="row" href="#/events/${esc(e.slug)}"><span><b>${esc(e.title)}</b>${next && next.slug === e.slug ? ' <span class="badge badge--ok">On the Events page</span>' : ''}<br><small>${esc(fmtDate(e.date))} · ${esc(fmtTime(e.time))}</small></span>${ic('arrow')}</a>`).join('') || '<p class="muted">Nothing coming up.</p>'}</div></div>
  <div class="card"><h2>Latest Journal posts</h2><p class="hint">Newest first.</p>
    <div class="rows">${S.posts.slice(0, 4).map(p => `<a class="row" href="#/journal/${esc(p.slug)}"><span><span class="badge ${p.draft ? '' : 'badge--dark'}">${p.draft ? 'Draft' : 'Published'}</span> &nbsp;${esc(p.title)}</span><small>${esc(p.date)}</small></a>`).join('') || '<p class="muted">No posts yet.</p>'}</div>
    <p style="margin:14px 0 0"><a class="btn" href="#/journal/new">${ic('plus')} New post</a></p></div>`;
  S.view = { files: [] };
  return shell('dashboard', body);
}
function fmtDate(d) { if (!d) return ''; const [y, m, dd] = d.split('-').map(Number); return new Date(y, m - 1, dd).toLocaleDateString('en-CA', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' }); }
function fmtTime(t) { if (!t) return ''; const [h, m] = t.split(':').map(Number); return `${h % 12 || 12}${m ? ':' + String(m).padStart(2, '0') : ''} ${h < 12 ? 'AM' : 'PM'}`; }

// ---------- events ----------
const isPast = e => e.date < today();
async function eventsList() {
  S.events = (await api('events')).events;
  await load(EVENTS);
  const f = EVENTS;
  const s = S.files[f].data.slots;
  const up = S.events.filter(e => !e.draft && !isPast(e)).sort((a, b) => (a.date + a.time).localeCompare(b.date + b.time));
  const shown = up.find(e => e.featured) || up[0];
  const rows = S.events.map(e => {
    const st = e.draft ? ['Draft', ''] : isPast(e) ? ['Past', ''] : ['Upcoming', 'badge--dark'];
    return `<tr><td><div class="thumb" style="background-image:url('${esc(thumbs(e.photo)[0] || '')}')"></div></td>
      <td><a href="#/events/${esc(e.slug)}">${esc(e.title)}</a>${shown && shown.slug === e.slug ? ' <span class="badge badge--ok" style="margin-left:6px">On the Events page</span>' : ''}<br><small class="muted">${esc(e.title_it)}</small></td>
      <td>${esc(fmtDate(e.date))}<br><small class="muted">${esc(fmtTime(e.time))}</small></td>
      <td><span class="badge ${st[1]}">${st[0]}</span></td>
      <td>${e.draft ? '' : `<a class="btn btn--sm btn--ghost" href="/events/${esc(e.slug)}/" target="_blank" rel="noopener" aria-label="View">${ic('ext')}</a>`}</td></tr>`;
  }).join('');
  const rooms = [1, 2, 3, 4].map(i => `<div class="card" style="box-shadow:none"><h2 style="font-size:15px">${esc((s[`events.room${i}.name`] || {}).en)}</h2><p class="hint"></p>
      ${pair('Name', f, ['slots', `events.room${i}.name`])}
      ${pair('One line about it', f, ['slots', `events.room${i}.lede`])}
      ${pair('How many guests', f, ['slots', `events.room${i}.cap`], { note: 'Also shown in the enquiry form' })}</div>`).join('');
  const incl = (s['events.incl.items'] || { items: [] }).items;
  const body = head('Events', 'Add events, and edit the Events page.', `<a class="btn" href="/events/" target="_blank" rel="noopener">${ic('ext')} View page</a><a class="btn btn--dark" href="#/events/new">${ic('plus')} New event</a>`) + `
  <div class="card" style="padding:8px 10px"><table class="table"><thead><tr><th></th><th>Event</th><th>When</th><th>Status</th><th></th></tr></thead><tbody>
  ${rows || '<tr><td colspan="5" class="muted">No events yet.</td></tr>'}</tbody></table></div>
  <p class="help" style="margin:-8px 0 26px">The dark panel on the Events page shows the event marked “Show on the Events page”, or else the next one coming up. When more than one event is coming up, the others are listed under it. Past events leave the Events page by themselves the next morning; their own page stays up without the booking button.</p>
  <div class="card"><h2>Top of the Events page</h2><p class="hint">The two short lines beside the title.</p>
    ${pair('First line', f, ['slots', 'events.hero.sub1'])}${pair('Second line', f, ['slots', 'events.hero.sub2'])}
    ${imageField('Photo', f, 'events.hero.image')}</div>
  <div class="card"><h2>The four spaces</h2><p class="hint">Names and sizes of the rooms. The drawings stay the same.</p><div class="grid2">${rooms}</div></div>
  <div class="card"><h2>What's included</h2><p class="hint">The short list under the spaces.</p>
    ${pair('Heading', f, ['slots', 'events.incl.title'])}
    ${incl.map((x, i) => `<div style="display:grid;grid-template-columns:1fr auto;gap:10px;align-items:end">${pair(`Line ${i + 1}`, f, ['slots', 'events.incl.items', 'items', i])}
      <button class="btn btn--icon btn--ghost btn--danger" type="button" data-incl-del="${i}" aria-label="Remove line" style="margin-bottom:14px">${ic('trash')}</button></div>`).join('')}
    <button class="btn" type="button" id="incl-add">${ic('plus')} Add a line</button></div>`;
  S.view = { title: 'Events page', files: [f], message: () => 'Update the Events page',
    wire: () => {
      $('#incl-add').onclick = () => { s['events.incl.items'].items.push({ en: '', it: '' }); render(); };
      $$('[data-incl-del]').forEach(b => { b.onclick = () => { s['events.incl.items'].items.splice(+b.dataset.inclDel, 1); render(); }; });
    } };
  return shell('events', body);
}

function blankEvent() {
  const L = () => ({ title: '', panel_title: '', summary: '', menu_line: '', cta: '', panel_cta: '', intro_html: '', after_html: '',
    photo_alt: '', seo_title: '', seo_description: '' });
  return { slug: '', draft: true, featured: false, date: '', time: '19:00', photo: { desk: '', mob: '', w: 0, h: 0 }, en: L(), it: L() };
}

async function eventEditor(slug) {
  if (!S.events) S.events = (await api('events')).events;
  let f;
  if (slug === 'new') { f = 'new-event'; if (!S.files[f]) S.files[f] = { data: blankEvent(), sha: null, orig: '' }; }
  else { f = `content/events/${slug}.json`; await load(f); }
  const d = S.files[f].data;
  d.photo = d.photo || { desk: '', mob: '' };
  const E = k => [k];
  const ph = (label, p, role) => photoCard(label, f, p, role, d.en.photo_alt);
  const body = head(slug === 'new' ? 'New event' : (d.en.title || 'Event'),
    slug === 'new' ? 'Fill it in, in English and Italian, then publish.' : (d.draft ? 'Draft: not on the website yet.' : (d.date < today() ? 'This event has passed.' : 'Published on the website.')),
    `<a class="btn" href="#/events">Back to events</a>${!d.draft && d.slug ? `<a class="btn" href="/events/${esc(d.slug)}/" target="_blank" rel="noopener">${ic('ext')} View</a>` : ''}`) + `
  <div class="editor"><div>
    <div class="card"><h2>The event</h2><p class="hint"></p>
      <div class="f"><span class="f__l">Name</span><div class="pair"><label><span class="lang">EN</span>${input(f, ['en', 'title'])}</label><label><span class="lang">IT</span>${input(f, ['it', 'title'])}</label></div></div>
      <div class="grid2">${field('Date', f, ['date'], { type: 'date' })}${field('Time', f, ['time'], { type: 'time' })}</div>
      <div class="f"><span class="f__l">Short description<small>On the Events page and in the list of events</small></span><div class="pair"><label><span class="lang">EN</span>${input(f, ['en', 'summary'], { rows: 3 })}</label><label><span class="lang">IT</span>${input(f, ['it', 'summary'], { rows: 3 })}</label></div></div>
      <div class="f"><span class="f__l">What's on the menu<small>e.g. Five courses</small></span><div class="pair"><label><span class="lang">EN</span>${input(f, ['en', 'menu_line'])}</label><label><span class="lang">IT</span>${input(f, ['it', 'menu_line'])}</label></div></div>
      <div class="f"><span class="f__l">About the evening<small>On the event's own page</small></span><div class="pair">
        <div><span class="lang">EN</span>${rich(f, ['en', 'intro_html'], true)}</div><div><span class="lang">IT</span>${rich(f, ['it', 'intro_html'], true)}</div></div></div>
      <div class="f"><span class="f__l">Button<small>Goes to the reservation page. Leave empty for “Reserve a Table”</small></span><div class="pair"><label><span class="lang">EN</span>${input(f, ['en', 'cta'], { ph: 'Reserve your seat' })}</label><label><span class="lang">IT</span>${input(f, ['it', 'cta'], { ph: 'Prenota il tuo posto' })}</label></div></div>
      <div class="f"><span class="f__l">Extra note under the button<small>Optional</small></span><div class="pair">
        <div><span class="lang">EN</span>${rich(f, ['en', 'after_html'], true)}</div><div><span class="lang">IT</span>${rich(f, ['it', 'after_html'], true)}</div></div></div>
    </div>
    <div class="card"><h2>On the Events page</h2><p class="hint">How it looks in the dark panel. Leave these empty to use the name and button above.</p>
      <div class="f"><span class="f__l">Name in the panel</span><div class="pair"><label><span class="lang">EN</span>${input(f, ['en', 'panel_title'], { ph: d.en.title })}</label><label><span class="lang">IT</span>${input(f, ['it', 'panel_title'], { ph: d.it.title })}</label></div></div>
      <div class="f"><span class="f__l">Button in the panel</span><div class="pair"><label><span class="lang">EN</span>${input(f, ['en', 'panel_cta'], { ph: d.en.cta || 'Reserve your table' })}</label><label><span class="lang">IT</span>${input(f, ['it', 'panel_cta'], { ph: d.it.cta || 'Prenota il tuo tavolo' })}</label></div></div>
    </div>
  </div>
  <div>
    <div class="card"><h2>Publishing</h2><p class="hint"></p>
      <label class="check" style="margin-bottom:10px"><input type="checkbox" id="pub" ${d.draft ? '' : 'checked'}> Published on the website</label>
      <label class="check" style="margin-bottom:14px"><input type="checkbox" id="feat" ${d.featured ? 'checked' : ''}> Show on the Events page</label>
      ${slug === 'new' ? `<label class="f"><span class="f__l">Web address<small>Made from the English name</small></span><input class="in" id="slug" value="${esc(d.slug || slugify(d.en.title))}" placeholder="made-from-the-name"></label>` : `<p class="help">Address: /events/${esc(d.slug)}/</p>`}
      <div class="btns">${slug !== 'new' ? `<button class="btn btn--danger" type="button" id="del">${ic('trash')} Delete</button>` : ''}</div>
    </div>
    <div class="card"><h2>Photo</h2><p class="hint">At the top of the event's page and in the panel.</p>
      <div class="imgfield" style="grid-template-columns:1fr 1fr">${ph('Computer', ['photo'], 'desk')}${ph('Phone', ['photo'], 'mob')}</div>
      <div class="f"><span class="f__l">Describe the photo</span><div class="pair" style="grid-template-columns:1fr"><label><span class="lang">EN</span>${input(f, ['en', 'photo_alt'])}</label><label><span class="lang">IT</span>${input(f, ['it', 'photo_alt'])}</label></div></div>
      <p class="help">No phone photo? The computer one is used on phones too.</p></div>
    <div class="card"><h2>Google</h2><p class="hint">Optional. Made from the name and description if left empty.</p>
      ${field('Search title (EN)', f, ['en', 'seo_title'], { max: 60, ph: d.en.title ? d.en.title + ' | Amami Italia' : '' })}
      ${field('Search description (EN)', f, ['en', 'seo_description'], { rows: 3, max: 160, ph: d.en.summary })}
      ${field('Search title (IT)', f, ['it', 'seo_title'], { max: 60, ph: d.it.title ? d.it.title + ' | Amami Italia' : '' })}
      ${field('Search description (IT)', f, ['it', 'seo_description'], { rows: 3, max: 160, ph: d.it.summary })}</div>
  </div></div>`;
  S.view = {
    title: 'event', files: [f],
    onInput: (el, p) => { if (p[0] === 'en' && p[1] === 'title' && slug === 'new' && $('#slug') && !S.slugTouched) $('#slug').value = slugify(el.value); },
    check: () => {
      const e = [];
      const nd = S.files[f].data;
      if (slug === 'new') {
        const sl = slugify($('#slug') ? $('#slug').value : nd.en.title);
        if (!sl) e.push('Give the event an English name first.');
        else if (S.events.some(x => x.slug === sl) || ['index'].includes(sl)) e.push('An event with that web address already exists. Change the name or the address.');
        nd.slug = sl;
        S.view.pathFor = k => (k === f ? `content/events/${sl}.json` : k);
      }
      if (!nd.en.title.trim()) e.push('The English name is missing.');
      if (!nd.it.title.trim()) e.push('Il nome in italiano manca (the Italian name is missing).');
      if (!nd.date) e.push('Choose the date.');
      if (!nd.time) e.push('Choose the time.');
      if (!nd.draft) {
        if (!nd.photo.desk) e.push('Add a photo before publishing.');
        for (const l of ['en', 'it']) if (!String(nd[l].summary || '').trim()) e.push(`The ${l === 'en' ? 'English' : 'Italian'} short description is empty.`);
        for (const l of ['en', 'it']) if (!String(nd[l].menu_line || '').trim()) e.push(`Fill in "What's on the menu" (${l === 'en' ? 'English' : 'Italian'}).`);
      }
      nd.modified = today();
      return e;
    },
    message: () => `${S.files[f].data.draft ? 'Save event draft' : 'Publish event'}: ${S.files[f].data.en.title}`.slice(0, 110),
    after: async () => {
      const nd = S.files[f].data;
      if (nd.featured) {           // only one event is "on the Events page"
        for (const ev of (S.events || []).filter(x => x.featured && x.slug !== nd.slug)) {
          const pth = `content/events/${ev.slug}.json`;
          await load(pth, true); S.files[pth].data.featured = false; await save(pth, `Events page now shows ${nd.en.title}`);
        }
      }
      if (slug === 'new') {
        const path = `content/events/${nd.slug}.json`;
        S.files[path] = S.files[f]; delete S.files[f];
        S.slugTouched = false;
        location.hash = `#/events/${nd.slug}`;
      }
      S.events = null;
    },
    wire: () => {
      $('#pub').onchange = e => { S.files[f].data.draft = !e.target.checked; paintSaveBar(); };
      $('#feat').onchange = e => { S.files[f].data.featured = e.target.checked; paintSaveBar(); };
      if ($('#slug')) $('#slug').oninput = () => { S.slugTouched = true; };
      if ($('#del')) $('#del').onclick = async () => {
        if (!confirm(`Delete "${d.en.title}"? Its page comes off the website in English and Italian.`)) return;
        try {
          const j = await api('content', { method: 'DELETE', body: { path: f, sha: S.files[f].sha } });
          S.pending = { commit: j.commit, since: Date.now() }; watchStatus();
          delete S.files[f]; S.events = null;
          toast('Event deleted. It comes off the website in about a minute.');
          location.hash = '#/events';
        } catch (err) { toast(err.message, true); }
      };
      wireRich();
    },
  };
  return shell('events', body);
}

// ---------- leads ----------
const SPACES = [['The Private Room', 'Private Room'], ['The Lounge', 'Lounge'], ['The Long Table', 'Long Table'], ['Full Buyout', 'Full Buyout'], ['Not sure yet', 'Not sure yet']];
async function loadLeads(force) {
  if (!S.leads || force) { const j = await api('leads'); S.leads = j.leads; S.statuses = j.statuses; }
  return S.leads;
}
async function leads(folder) {
  let list = [], err = '';
  try { list = await loadLeads(); } catch (e) { err = e.message; }
  const fold = decodeURIComponent(folder || 'all');
  const inFolder = (l, k) => k === 'all' || (l.space || 'Not sure yet') === k || (k === 'Not sure yet' && !SPACES.some(s => s[0] === l.space));
  const chips = [['all', 'All'], ...SPACES].map(([k, t]) => {
    const n = list.filter(l => inFolder(l, k)).length, nw = list.filter(l => inFolder(l, k) && l.status === 'New').length;
    return `<a class="chip" href="#/leads/${encodeURIComponent(k)}" ${fold === k ? 'aria-current="page"' : ''}>${esc(t)} <b>${n}</b>${nw ? '<span class="dot" style="color:#dc2626"></span>' : ''}</a>`;
  }).join('');
  const q = (S.leadQ || '').toLowerCase();
  const shown = list.filter(l => inFolder(l, fold) && (!q || JSON.stringify(l).toLowerCase().includes(q)));
  const card = l => {
    const name = [l.firstName, l.lastName].filter(Boolean).join(' ') || l.name || l.email;
    return `<div class="card lead" style="margin-bottom:12px">
      <div style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;align-items:flex-start">
        <div><div class="btns" style="margin-bottom:6px"><span class="badge">${esc(l.space || 'Not sure yet')}</span>${l.status === 'New' ? '<span class="badge badge--dark">New</span>' : ''}</div>
          <b style="font-size:16px">${esc(name)}</b><div class="muted" style="font-size:14px">${esc(l.email)}${l.phone ? ' · ' + esc(l.phone) : ''}</div></div>
        <div style="text-align:right"><small class="muted">${esc(l.received ? new Date(l.received).toLocaleString('en-CA', { dateStyle: 'medium', timeStyle: 'short' }) : '')}</small><br>
          <select class="in" style="width:auto;margin-top:6px" data-lead="${esc(l.row)}">${(S.statuses || ['New', 'Contacted', 'Booked', 'Not going ahead']).map(st => `<option ${st === l.status ? 'selected' : ''}>${esc(st)}</option>`).join('')}</select></div></div>
      <div class="grid3" style="margin-top:14px;font-size:14px"><div><small class="muted">Event date</small><br>${esc(l.date ? String(l.date).slice(0, 10) : '—')}</div><div><small class="muted">Guests</small><br>${esc(l.guests || '—')}</div><div><small class="muted">From page</small><br>${esc(l.page || '—')}</div></div>
      ${l.message ? `<p style="margin:14px 0 0;white-space:pre-wrap">${esc(l.message)}</p>` : ''}
      <div class="btns" style="margin-top:14px"><a class="btn btn--sm" href="mailto:${esc(l.email)}?subject=${encodeURIComponent('Your event enquiry at Amami Italia')}">Reply by email</a>${l.phone ? `<a class="btn btn--sm" href="tel:${esc(String(l.phone).replace(/[^+\d]/g, ''))}">Call</a>` : ''}</div></div>`;
  };
  const body = head('Leads', 'Every event enquiry from the website, by space. Pick a folder to focus on one.', `<button class="btn" type="button" id="lead-refresh">Refresh</button>`) + `
  ${err ? `<div class="notice notice--bad">${esc(err)}</div>` : ''}
  <div class="chips">${chips}</div>
  <div class="btns" style="margin:0 0 18px"><label class="search" style="position:relative;flex:1"><input class="in" id="lq" placeholder="Search name, email, message" value="${esc(S.leadQ || '')}" style="padding-left:34px"><span style="position:absolute;left:10px;top:10px;color:var(--ink-3)">${ic('search')}</span></label></div>
  ${shown.map(card).join('') || (err ? '' : '<p class="muted">No enquiries here yet.</p>')}`;
  S.view = { files: [], wire: () => {
    $('#lead-refresh').onclick = async () => { try { await loadLeads(true); render(); } catch (e) { toast(e.message, true); } };
    $('#lq').oninput = e => { S.leadQ = e.target.value; const pos = e.target.selectionStart; render(); const n = $('#lq'); n.focus(); n.setSelectionRange(pos, pos); };
    $$('[data-lead]').forEach(sel => { sel.onchange = async () => {
      const l = S.leads.find(x => String(x.row) === sel.dataset.lead);
      try { await api('leads', { method: 'POST', body: { row: l.row, status: sel.value } }); l.status = sel.value; toast(`Marked as ${sel.value}.`); render(); }
      catch (e) { toast(e.message, true); sel.value = l.status; }
    }; });
  } };
  return shell('leads', body);
}

// ---------- rich text (Journal writing, event page) ----------
function rich(f, p, small) {
  const v = getIn(S.files[f].data, p) || '';
  return `<div class="rt-wrap" data-f="${esc(f)}" data-p="${P(p)}"><div class="rt-bar">
    ${small ? '' : '<button type="button" data-cmd="h2" title="Heading">H2</button><button type="button" data-cmd="h3" title="Small heading">H3</button>'}
    <button type="button" data-cmd="p" title="Normal text">¶</button>
    <button type="button" data-cmd="bold" title="Bold"><b>B</b></button><button type="button" data-cmd="italic" title="Italic"><i>I</i></button>
    <button type="button" data-cmd="link" title="Link">Link</button>
    ${small ? '' : '<button type="button" data-cmd="ul" title="Bulleted list">• List</button><button type="button" data-cmd="ol" title="Numbered list">1. List</button><button type="button" data-cmd="quote" title="Pull quote">Quote</button>'}
    <button type="button" data-cmd="clear" title="Remove formatting">Clear</button>
    <button type="button" data-cmd="html" title="Edit the HTML" style="margin-left:auto">HTML</button></div>
    <div class="rt" contenteditable="true" style="${small ? 'min-height:160px' : ''}">${v}</div></div>`;
}
function tidy(html) {
  const d = document.createElement('div');
  d.innerHTML = html;
  d.querySelectorAll('[style]').forEach(n => n.removeAttribute('style'));
  d.querySelectorAll('b').forEach(n => { const s = document.createElement('strong'); s.innerHTML = n.innerHTML; n.replaceWith(s); });
  d.querySelectorAll('i').forEach(n => { const s = document.createElement('em'); s.innerHTML = n.innerHTML; n.replaceWith(s); });
  d.querySelectorAll('span:not([class])').forEach(n => n.replaceWith(...n.childNodes));
  d.querySelectorAll('font').forEach(n => n.replaceWith(...n.childNodes));
  [...d.childNodes].forEach(n => {           // loose text and <div>s become paragraphs
    if (n.nodeType === 3 && n.textContent.trim()) { const p = document.createElement('p'); p.textContent = n.textContent; n.replaceWith(p); }
    else if (n.nodeName === 'DIV' && !n.className) { const p = document.createElement('p'); p.innerHTML = n.innerHTML; n.replaceWith(p); }
  });
  return d.innerHTML.replace(/<p><br><\/p>/g, '').replace(/&nbsp;/g, ' ').trim();
}
function wireRich() {
  $$('.rt-wrap').forEach(w => {
    const ed = $('.rt', w), f = w.dataset.f, p = JSON.parse(w.dataset.p);
    const push = () => { setIn(S.files[f].data, p, tidy(ed.innerHTML)); paintSaveBar(); };
    ed.addEventListener('input', push);
    ed.addEventListener('paste', e => {
      e.preventDefault();
      const t = (e.clipboardData || window.clipboardData).getData('text/plain');
      const html = t.split(/\n{2,}/).map(x => `<p>${esc(x).replace(/\n/g, '<br>')}</p>`).join('');
      document.execCommand('insertHTML', false, html);
    });
    $$('[data-cmd]', w).forEach(b => b.addEventListener('mousedown', e => e.preventDefault()));
    $$('[data-cmd]', w).forEach(b => b.addEventListener('click', () => {
      const c = b.dataset.cmd;
      ed.focus();
      if (c === 'html') {
        const cur = getIn(S.files[f].data, p) || '';
        const ta = document.createElement('textarea');
        ta.className = 'in src'; ta.value = cur;
        const done = document.createElement('button');
        done.type = 'button'; done.className = 'btn btn--sm'; done.textContent = 'Back to the editor';
        ed.replaceWith(ta); ta.after(done); b.disabled = true;
        ta.oninput = () => { setIn(S.files[f].data, p, ta.value); paintSaveBar(); };
        done.onclick = () => { ed.innerHTML = ta.value; ta.replaceWith(ed); done.remove(); b.disabled = false; };
        return;
      }
      if (c === 'bold' || c === 'italic') document.execCommand(c);
      else if (c === 'h2' || c === 'h3' || c === 'p') document.execCommand('formatBlock', false, c.toUpperCase());
      else if (c === 'ul') document.execCommand('insertUnorderedList');
      else if (c === 'ol') document.execCommand('insertOrderedList');
      else if (c === 'clear') { document.execCommand('removeFormat'); document.execCommand('formatBlock', false, 'P'); }
      else if (c === 'quote') {
        document.execCommand('formatBlock', false, 'P');
        const sel = getSelection(); const el = sel.anchorNode && (sel.anchorNode.nodeType === 1 ? sel.anchorNode : sel.anchorNode.parentElement).closest('p');
        if (el && ed.contains(el)) el.classList.toggle('pull');
      } else if (c === 'link') {
        const url = prompt('Link to (for example /menu/ or https://…):', '/');
        if (url) document.execCommand('createLink', false, url.trim());
      }
      push();
    }));
  });
}

// ---------- menu ----------
const MENUS = [['dining', 'Pranzo e Cena'], ['pizza', 'Pizza'], ['cocktails', 'Cocktails'], ['after-dark', 'After Dark']];
async function menu(page) {
  await load(MENU);
  const f = MENU;
  page = MENUS.some(m => m[0] === page) ? page : 'dining';
  const m = S.files[f].data.menus[page];
  const q = (S.menuQ || '').toLowerCase();
  const secs = m.sections.map((sec, si) => {
    const rows = sec.items.map((it, ii) => {
      const p = ['menus', page, 'sections', si, 'items', ii];
      const hit = !q || [it.name, it.desc && it.desc.en, it.desc && it.desc.it].join(' ').toLowerCase().includes(q);
      return `<div class="dish" ${hit ? '' : 'hidden'}>
        <div class="dish__move"><button class="btn btn--icon btn--ghost" type="button" data-mv="${si},${ii},-1" aria-label="Move up" ${ii ? '' : 'disabled'}>${ic('up')}</button>
          <button class="btn btn--icon btn--ghost" type="button" data-mv="${si},${ii},1" aria-label="Move down" ${ii < sec.items.length - 1 ? '' : 'disabled'}>${ic('down')}</button></div>
        <label><span class="f__l">Name</span>${input(f, [...p, 'name'])}</label>
        <label class="dish__price"><span class="f__l">Price</span>${input(f, [...p, 'price'], { ph: '18' })}</label>
        <div class="dish__del"><button class="btn btn--icon btn--ghost btn--danger" type="button" data-del="${si},${ii}" aria-label="Delete ${esc(it.name)}">${ic('trash')}</button></div>
        <div class="dish__more">
          <label><span class="f__l"><span><span class="lang">EN</span>Description</span></span>${input(f, [...p, 'desc', 'en'], { rows: 2 })}</label>
          <label><span class="f__l"><span><span class="lang">IT</span>Descrizione</span></span>${input(f, [...p, 'desc', 'it'], { rows: 2 })}</label>
          <label><span class="f__l"><span><span class="lang">EN</span>Add-on</span><small>optional, e.g. Add shrimp 8</small></span>${input(f, [...p, 'add', 'en'])}</label>
          <label><span class="f__l"><span><span class="lang">IT</span>Aggiunta</span></span>${input(f, [...p, 'add', 'it'])}</label>
          <div class="dish__tags">${check('Vegetarian (V)', f, [...p, 'v'])}${check('Gluten free (GF)', f, [...p, 'gf'])}</div>
        </div></div>`;
    }).join('');
    return `<div class="card"><h2>${esc(sec.title)}</h2><p class="hint">${sec.items.length} item${sec.items.length === 1 ? '' : 's'}</p>${rows}
      <button class="btn" type="button" data-add="${si}">${ic('plus')} Add to ${esc(sec.title)}</button></div>`;
  }).join('');
  const hero = (S.files[f].data.slots || {})[`menu.${page}.hero`];
  const body = head('Menu', 'Names, descriptions and prices. Changes show on the menu pages.', `<a class="btn" href="/menu/${page}/" target="_blank" rel="noopener">${ic('ext')} View page</a>`) + `
  <div class="tabs" role="tablist">${MENUS.map(([k, t]) => `<a href="#/menu/${k}" ${k === page ? 'aria-current="page"' : ''}>${esc(t)}</a>`).join('')}</div>
  <div class="btns" style="margin-bottom:18px"><label class="search" style="position:relative;flex:1"><input class="in" id="mq" placeholder="Find a dish" value="${esc(S.menuQ || '')}" style="padding-left:34px"><span style="position:absolute;left:10px;top:10px;color:var(--ink-3)">${ic('search')}</span></label></div>
  ${secs}
  ${hero ? `<div class="card"><h2>Photo at the top of this menu</h2><p class="hint"></p>${imageField('Photo', f, `menu.${page}.hero`)}</div>` : ''}`;
  S.view = { title: 'menu', files: [f], message: () => `Update the ${MENUS.find(x => x[0] === page)[1]} menu`,
    check: () => {
      for (const [k, t] of MENUS) for (const sec of S.files[f].data.menus[k].sections) for (const it of sec.items) {
        if (!String(it.name || '').trim()) return [`A dish in ${t} → ${sec.title} has no name.`];
        it.price = String(it.price || '').trim().replace(/^\$\s*/, '');
      }
      return [];
    },
    wire: () => {
      $('#mq').oninput = e => { S.menuQ = e.target.value; const pos = e.target.selectionStart; render(); const n = $('#mq'); n.focus(); n.setSelectionRange(pos, pos); };
      $$('[data-add]').forEach(b => { b.onclick = () => { m.sections[+b.dataset.add].items.push({ name: '', price: '', v: false, gf: false, desc: { en: '', it: '' }, add: { en: '', it: '' } }); render(); const all = $$('.card')[+b.dataset.add]; const ins = all && $$('.dish input', all); if (ins && ins.length) ins[ins.length - 4] && ins[ins.length - 4].focus(); }; });
      $$('[data-del]').forEach(b => { b.onclick = () => { const [si, ii] = b.dataset.del.split(',').map(Number); const it = m.sections[si].items[ii]; if (confirm(`Remove ${it.name || 'this dish'} from the menu?`)) { m.sections[si].items.splice(ii, 1); render(); } }; });
      $$('[data-mv]').forEach(b => { b.onclick = () => { const [si, ii, d] = b.dataset.mv.split(',').map(Number); const a = m.sections[si].items; [a[ii], a[ii + d]] = [a[ii + d], a[ii]]; render(); }; });
    } };
  return shell('menu', body);
}

// ---------- photos ----------
async function photos() {
  await Promise.all([load(EVENTS), load(MENU)]);
  if (!S.posts) S.posts = (await api('posts')).posts;
  const E = EVENTS, M = MENU;
  const groups = [
    ['Events page', E, [['events.hero.image', 'Top of the page']]],
    ['Menu page', M, [['menu.hero.image', 'Top of the page'], ['menu.card1.image', 'Card 1 · Pranzo e Cena'], ['menu.card2.image', 'Card 2 · La Cantina'], ['menu.card3.image', 'Card 3 · Dal Forno'], ['menu.card4.image', 'Card 4 · Cocktails']]],
    ['Menu pages', M, MENUS.map(([k, t]) => [`menu.${k}.hero`, t])],
  ];
  const body = head('Photos', 'Replace the photos on the Events and Menu pages. Event and Journal photos are changed in each event or post.') +
    groups.map(([t, f, list]) => `<div class="card"><h2>${esc(t)}</h2><p class="hint"></p>${list.filter(([k]) => S.files[f].data.slots[k]).map(([k, l]) => imageField(l, f, k)).join('<hr class="sep">')}</div>`).join('') +
    `<div class="card"><h2>Journal</h2><p class="hint">Open a post to change its photo.</p><div class="photos">${S.posts.map(p => `<a class="ph" href="#/journal/${esc(p.slug)}" style="text-decoration:none">${imgTag(p.photo, p.title)}<div class="ph__b"><b>${esc(p.title)}</b>${ic('arrow')}</div></a>`).join('')}</div></div>`;
  S.view = { title: 'photos', files: [E, M], message: () => 'Update page photos' };
  return shell('photos', body);
}

// ---------- journal ----------
async function journal() {
  S.posts = (await api('posts')).posts;
  const cats = (await load(CATS)).data;
  const body = head('Journal', 'Write and publish posts. They appear in English and Italian.', `<a class="btn btn--dark" href="#/journal/new">${ic('plus')} New post</a>`) + `
  <div class="card" style="padding:8px 10px"><table class="table"><thead><tr><th></th><th>Title</th><th>Category</th><th>Date</th><th>Status</th><th></th></tr></thead><tbody>
  ${S.posts.map(p => `<tr><td><div class="thumb" style="background-image:url('${esc(thumbs(p.photo)[0] || '')}')"></div></td>
    <td><a href="#/journal/${esc(p.slug)}">${esc(p.title)}</a><br><small class="muted">${esc(p.title_it)}</small></td>
    <td>${esc((cats[p.category] || {}).en || p.category)}</td><td>${esc(p.date)}</td>
    <td><span class="badge ${p.draft ? '' : 'badge--dark'}">${p.draft ? 'Draft' : 'Published'}</span></td>
    <td>${p.draft ? '' : `<a class="btn btn--sm btn--ghost" href="/journal/${esc(p.slug)}/" target="_blank" rel="noopener" aria-label="View">${ic('ext')}</a>`}</td></tr>`).join('') || '<tr><td colspan="6" class="muted">No posts yet.</td></tr>'}
  </tbody></table></div>`;
  S.view = { files: [] };
  return shell('journal', body);
}

function blankPost(cat) {
  const lang = () => ({ title: '', dek: '', excerpt: '', body_html: '', photo_alt: '', seo_title: '', seo_description: '', focus_keyword: '', keywords: '', faq: [] });
  return { slug: '', path: '', date: today(), modified: today(), category: cat, draft: true, layout: 'journal',
    author: { '@type': 'Organization', name: 'Amami Italia' }, photo: { base: '', width: 0, height: 0 }, en: lang(), it: lang() };
}

async function post(slug) {
  const cats = await load(CATS);
  if (!S.posts) S.posts = (await api('posts')).posts;
  let f;
  if (slug === 'new') {
    f = 'new-post';
    if (!S.files[f]) S.files[f] = { data: blankPost(Object.keys(cats.data)[0]), sha: null, orig: '' };
  } else {
    f = `content/journal/posts/${slug}.json`;
    await load(f);
  }
  const d = S.files[f].data;
  const lg = S.postLang || 'en';
  const lp = k => [lg, k];
  const seoT = (d[lg] || {}).seo_title || (d[lg] || {}).title || '';
  const seoD = (d[lg] || {}).seo_description || (d[lg] || {}).excerpt || '';
  const url = `amamiitalia.etherealpr.com${lg === 'it' ? '/it' : ''}/journal/${d.slug || slugify(d.en.title) || 'your-post'}/`;
  const faq = d[lg].faq || [];
  const done = l => d[l].title && d[l].body_html && d[l].excerpt;
  const body = head(slug === 'new' ? 'New post' : (d.en.title || 'Post'), slug === 'new' ? 'Write it in English and Italian, then publish.' : (d.draft ? 'Draft: not on the website yet.' : 'Published on the website.'),
    `<a class="btn" href="#/journal">Back to posts</a>${!d.draft && d.slug ? `<a class="btn" href="/journal/${esc(d.slug)}/" target="_blank" rel="noopener">${ic('ext')} View</a>` : ''}`) + `
  <div class="editor"><div>
    <div class="tabs" role="tablist">
      <button type="button" role="tab" data-lang="en" aria-selected="${lg === 'en'}">English ${done('en') ? '' : '<span class="badge badge--warn" style="margin-left:6px">to do</span>'}</button>
      <button type="button" role="tab" data-lang="it" aria-selected="${lg === 'it'}">Italiano ${done('it') ? '' : '<span class="badge badge--warn" style="margin-left:6px">da fare</span>'}</button></div>
    <div class="card">
      ${field('Title', f, lp('title'), { note: 'Shown on the post and the Journal list' })}
      ${field('Subtitle', f, lp('dek'), { note: 'One line under the title' })}
      ${field('Summary for the Journal list', f, lp('excerpt'), { rows: 2, note: 'One sentence' })}
      <div class="f"><span class="f__l">The writing<small>Headings, bold, italic, links, lists and quotes</small></span>${rich(f, lp('body_html'))}</div>
    </div>
    <div class="card"><h2>Questions and answers</h2><p class="hint">Optional. Google can show these under the post in search results.</p>
      ${faq.map((x, i) => `<div style="display:grid;grid-template-columns:1fr auto;gap:10px">${'<div>' + field('Question', f, [lg, 'faq', i, 'q']) + field('Answer', f, [lg, 'faq', i, 'a'], { rows: 2 }) + '</div>'}
        <button class="btn btn--icon btn--ghost btn--danger" type="button" data-faq-del="${i}" aria-label="Remove question">${ic('trash')}</button></div><hr class="sep">`).join('')}
      <button class="btn" type="button" id="faq-add">${ic('plus')} Add a question</button></div>
  </div>
  <div>
    <div class="card"><h2>Publishing</h2><p class="hint"></p>
      <label class="check" style="margin-bottom:14px"><input type="checkbox" id="pub" ${d.draft ? '' : 'checked'}> Published on the website</label>
      ${field('Date', f, ['date'], { type: 'date' })}
      <label class="f"><span class="f__l">Category</span><select class="in" id="cat">${Object.entries(cats.data).map(([k, c]) => `<option value="${esc(k)}" ${k === d.category ? 'selected' : ''}>${esc(c.en)} / ${esc(c.it)}</option>`).join('')}<option value="__new">+ New category…</option></select></label>
      ${field('Written by', f, ['author', 'name'])}
      ${slug === 'new' ? `<label class="f"><span class="f__l">Web address<small>Made from the English title</small></span><input class="in" id="slug" value="${esc(d.slug || slugify(d.en.title))}" placeholder="made-from-the-title"></label>` : `<p class="help">Address: /journal/${esc(d.slug)}/</p>`}
      <div class="btns">${slug !== 'new' ? `<button class="btn btn--danger" type="button" id="del">${ic('trash')} Delete</button>` : ''}</div>
    </div>
    <div class="card"><h2>Photo</h2><p class="hint">The banner at the top of the post and on the Journal list.</p>
      ${photoCard('Banner', f, ['photo'], 'post', d[lg].photo_alt)}
      <div style="height:12px"></div>${field('Describe the photo', f, lp('photo_alt'), { note: 'For Google' })}</div>
    <div class="card"><h2>Google</h2><p class="hint">How the post can look in search results.</p>
      <div class="serp"><div class="serp__u">${esc(url)}</div><div class="serp__t">${esc(seoT)}</div><div class="serp__d">${esc(seoD)}</div></div>
      ${field('Search title', f, lp('seo_title'), { max: 60, note: `${seoT.length}/60` })}
      ${field('Search description', f, lp('seo_description'), { rows: 3, max: 160, note: `${((d[lg] || {}).seo_description || '').length} of 120–155` })}
      ${field('Main search phrase', f, lp('focus_keyword'), { note: 'e.g. aperitivo Brampton' })}
      ${field('Other phrases', f, lp('keywords'), { note: 'Separated by commas' })}</div>
  </div></div>`;
  S.view = {
    title: 'post', files: [f],
    onInput: (el, p) => {
      if (p[0] === 'en' && p[1] === 'title' && slug === 'new' && $('#slug') && !S.slugTouched) $('#slug').value = slugify(el.value);
      if (p[1] === 'seo_title' || p[1] === 'seo_description') { const L2 = el.closest('label').querySelector('.f__l small'); if (L2) L2.textContent = p[1] === 'seo_title' ? `${el.value.length}/60` : `${el.value.length} of 120–155`; }
    },
    check: () => {
      const e = [];
      const nd = S.files[f].data;
      if (slug === 'new') {
        const sl = slugify($('#slug') ? $('#slug').value : nd.en.title);
        if (!sl) e.push('Give the post an English title first.');
        else if (S.posts.some(x => x.slug === sl)) e.push('A post with that web address already exists. Change the title or the address.');
        nd.slug = sl; nd.path = `journal/${sl}`;
        S.view.pathFor = k => (k === f ? `content/journal/posts/${sl}.json` : k);
      }
      if (!nd.en.title.trim()) e.push('The English title is missing.');
      if (!nd.it.title.trim()) e.push('Il titolo in italiano manca (the Italian title is missing).');
      if (!nd.draft) {
        if (!nd.photo.base) e.push('Add a banner photo before publishing.');
        for (const l of ['en', 'it']) if (!String(nd[l].body_html || '').replace(/<[^>]+>/g, '').trim()) e.push(`The ${l === 'en' ? 'English' : 'Italian'} writing is empty.`);
      }
      nd.modified = today();
      for (const l of ['en', 'it']) {
        nd[l].faq = (nd[l].faq || []).filter(x => x.q && x.a);
        if (!nd[l].faq.length) delete nd[l].faq;
        if (!nd[l].og_image) delete nd[l].og_image;
        nd[l].dek = String(nd[l].dek || '').replace(/<[^>]*>/g, '');
      }
      return e;
    },
    message: () => `${S.files[f].data.draft ? 'Save draft' : 'Publish'}: ${S.files[f].data.en.title}`.slice(0, 110),
    after: async () => {
      if (slug === 'new') {
        const nd = S.files[f].data;
        const path = `content/journal/posts/${nd.slug}.json`;
        S.files[path] = S.files[f]; delete S.files[f];
        S.posts = null; S.slugTouched = false;
        location.hash = `#/journal/${nd.slug}`;
      } else S.posts = null;
    },
    wire: () => {
      $$('[data-lang]').forEach(b => { b.onclick = () => { S.postLang = b.dataset.lang; render(); }; });
      $('#pub').onchange = e => { S.files[f].data.draft = !e.target.checked; paintSaveBar(); };
      if ($('#slug')) $('#slug').oninput = () => { S.slugTouched = true; };
      $('#cat').onchange = async e => {
        if (e.target.value !== '__new') { S.files[f].data.category = e.target.value; paintSaveBar(); return; }
        const en = prompt('New category name in English:'); if (!en) { e.target.value = d.category; return; }
        const it = prompt('The same category in Italian:', en) || en;
        const key = slugify(en);
        const n = Object.keys(cats.data).length + 1;
        cats.data[key] = { en, it, code: `AM/${String(n).padStart(2, '0')}` };
        S.files[f].data.category = key;
        if (!S.view.files.includes(CATS)) S.view.files.unshift(CATS);
        render();
      };
      $('#faq-add').onclick = () => { const L2 = S.files[f].data[lg]; (L2.faq = L2.faq || []).push({ q: '', a: '' }); render(); };
      $$('[data-faq-del]').forEach(b => { b.onclick = () => { S.files[f].data[lg].faq.splice(+b.dataset.faqDel, 1); render(); }; });
      if ($('#del')) $('#del').onclick = async () => {
        if (!confirm(`Delete "${d.en.title}"? It comes off the website in English and Italian. This cannot be undone from here.`)) return;
        try {
          const j = await api('content', { method: 'DELETE', body: { path: f, sha: S.files[f].sha } });
          S.pending = { commit: j.commit, since: Date.now() }; watchStatus();
          delete S.files[f]; S.posts = null;
          toast('Post deleted. It comes off the website in about a minute.');
          location.hash = '#/journal';
        } catch (err) { toast(err.message, true); }
      };
      wireRich();
    },
  };
  if (dirty(CATS)) S.view.files.unshift(CATS);
  return shell('journal', body);
}

// ---------- router ----------
let renderSeq = 0;
async function render() {
  const seq = ++renderSeq;
  if (!S.me) return loginView();
  const [, route = 'dashboard', arg] = (location.hash || '#/dashboard').split('/');
  if (route === 'signout') {
    if (anyDirty() && !confirm('You have unsaved changes. Sign out anyway?')) { history.back(); return; }
    await api('logout', { method: 'POST' }).catch(() => {});
    S.me = null; S.files = {}; S.posts = null; location.hash = '';
    return loginView();
  }
  const scroll = window.scrollY;
  try {
    const views = { dashboard, leads: () => leads(arg), events: () => (arg ? eventEditor(arg) : eventsList()), journal: () => (arg ? post(arg) : journal()), menu: () => menu(arg), photos };
    const html = await (views[route] || dashboard)();
    if (seq !== renderSeq) return;
    const prevRoute = S.lastRoute; S.lastRoute = location.hash;
    $('#app').innerHTML = html;
    document.title = `${(NAV.find(n => n[0] === route) || NAV[0])[1]} | Amami Italia Admin`;
    $('#save') && ($('#save').onclick = saveView);
    $('#discard') && ($('#discard').onclick = () => { if (confirm('Discard your changes on this page?')) discardView(); });
    if (S.view && S.view.wire) S.view.wire();
    if (!S.me.github) $('.main').insertAdjacentHTML('afterbegin', '<div class="notice notice--bad">Saving is switched off: the portal is not connected to GitHub yet.</div>');
    paintSaveBar();
    if (prevRoute === location.hash) window.scrollTo(0, scroll);
    else window.scrollTo(0, 0);
  } catch (err) {
    if (seq !== renderSeq) return;
    $('#app').innerHTML = shell(route, `<div class="notice notice--bad">${esc(err.message)}</div><button class="btn" onclick="location.reload()">Try again</button>`);
  }
}
window.addEventListener('hashchange', render);

(async () => {
  try { S.me = await api('me'); refreshStatus(); } catch (e) { S.me = null; }
  render();
})();
})();
