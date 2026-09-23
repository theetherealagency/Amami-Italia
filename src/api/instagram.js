// The footer's six "recent posts" frames, kept current without anyone touching
// the site. GET /api/instagram/ returns the latest posts of @amamiitalia_official
// as JSON; GET /api/instagram/?img=<url> streams one post image through this
// origin (Instagram's CDN links expire and are not meant for hotlinking).
//
// Source, in order:
//  1. The Instagram Graph API, when IG_TOKEN is set in the Vercel project's
//     environment (a long-lived Instagram token for the account). Most reliable.
//  2. Otherwise Instagram's public profile feed, the one instagram.com itself uses.
//     (As of 2026-09 Instagram answers this with 429 from cloud and home IPs alike,
//     so in practice the grid goes live once IG_TOKEN is set.)
// Vercel's edge caches the answer for an hour, so Instagram is asked at most once
// an hour. If both fail the page keeps the six photographs already in the HTML.

const USER = 'amamiitalia_official';
const COUNT = 6;
const IMG_HOSTS = /(^|\.)(cdninstagram\.com|fbcdn\.net)$/i;
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36';

// IG_TOKEN alone: an "Instagram Login" token (starts IGAA…, lasts 60 days).
// IG_TOKEN + IG_USER_ID: a Facebook Page / system-user token (starts EAA…) for the
// Instagram business account id — a system-user token does not expire.
async function fromGraph(token, userId) {
  const fields = 'fields=id,caption,media_type,media_url,thumbnail_url,permalink,timestamp&limit=12&access_token=' + encodeURIComponent(token);
  const u = userId ? 'https://graph.facebook.com/v21.0/' + encodeURIComponent(userId) + '/media?' + fields
                   : 'https://graph.instagram.com/me/media?' + fields;
  const r = await fetch(u);
  if (!r.ok) throw new Error('graph ' + r.status);
  const j = await r.json();
  return (j.data || []).map(m => ({
    link: m.permalink,
    img: m.media_type === 'VIDEO' ? m.thumbnail_url : m.media_url,
    alt: (m.caption || '').split('\n')[0].slice(0, 140),
    time: Date.parse(m.timestamp) / 1000
  }));
}

// the same public profile feed, asked the way the website and the Android app ask
const PROFILE_TRIES = [
  ['https://www.instagram.com/api/v1/users/web_profile_info/?username=' + USER,
    { 'x-ig-app-id': '936619743392459', 'user-agent': UA, 'accept': 'application/json', 'referer': 'https://www.instagram.com/' + USER + '/' }],
  ['https://i.instagram.com/api/v1/users/web_profile_info/?username=' + USER,
    { 'x-ig-app-id': '936619743392459', 'user-agent': 'Instagram 219.0.0.12.117 Android (31/12; 420dpi; 1080x2400; samsung; SM-G991B; o1s; exynos2100; en_US; 346138365)', 'accept': 'application/json' }]
];

async function fromProfile() {
  let j = null, why = [];
  for (const [u, h] of PROFILE_TRIES) {
    try {
      const r = await fetch(u, { headers: h, redirect: 'manual' });
      if (r.ok) { j = await r.json(); break; }
      why.push(new URL(u).hostname + ' ' + r.status);
    } catch (e) { why.push(new URL(u).hostname + ' ' + e.message); }
  }
  if (!j) throw new Error('profile: ' + why.join(', '));
  const edges = (((j.data || {}).user || {}).edge_owner_to_timeline_media || {}).edges || [];
  return edges.map(({ node: n }) => ({
    link: 'https://www.instagram.com/' + (n.is_video ? 'reel' : 'p') + '/' + n.shortcode + '/',
    img: n.thumbnail_src || n.display_url,
    alt: (((((n.edge_media_to_caption || {}).edges || [])[0] || {}).node || {}).text || n.accessibility_caption || '').split('\n')[0].slice(0, 140),
    time: n.taken_at_timestamp,
    pinned: Array.isArray(n.pinned_for_users) && n.pinned_for_users.length > 0
  }));
}

module.exports = async (req, res) => {
  const q = new URL(req.url, 'https://x').searchParams;

  // image relay: only Instagram's own CDN, never an open proxy
  const img = q.get('img');
  if (img) {
    let host = '';
    try { host = new URL(img).hostname; } catch (e) {}
    if (!IMG_HOSTS.test(host)) { res.statusCode = 400; return res.end('bad image host'); }
    try {
      const r = await fetch(img, { headers: { 'user-agent': UA } });
      if (!r.ok) { res.statusCode = 502; return res.end(); }
      res.setHeader('Content-Type', r.headers.get('content-type') || 'image/jpeg');
      res.setHeader('Cache-Control', 'public, max-age=86400, s-maxage=604800');
      return res.end(Buffer.from(await r.arrayBuffer()));
    } catch (e) { res.statusCode = 502; return res.end(); }
  }

  let posts = [], source = '', errors = [];
  try {
    if (process.env.IG_TOKEN) { posts = await fromGraph(process.env.IG_TOKEN, process.env.IG_USER_ID); source = 'graph'; }
  } catch (e) { posts = []; errors.push(e.message); }
  if (!posts.length) {
    try { posts = await fromProfile(); source = 'profile'; } catch (e) { posts = []; errors.push(e.message); }
  }
  // newest first by date, so a pinned older post doesn't hold a frame
  posts = posts.filter(p => p.img).sort((a, b) => b.time - a.time).slice(0, COUNT)
    .map(p => ({ link: p.link, alt: p.alt, img: '/api/instagram/?img=' + encodeURIComponent(p.img) }));

  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  // an empty answer is cached briefly, so a hiccup at Instagram clears itself
  res.setHeader('Cache-Control', posts.length ? 'public, s-maxage=3600, stale-while-revalidate=86400' : 'public, s-maxage=300');
  res.end(JSON.stringify({ source, posts, errors }));
};
