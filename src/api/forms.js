// Every form on the site posts here: POST /api/forms/ (urlencoded, from
// amami.js). Each submission is emailed to the info inbox through Resend,
// sent from the verified amamiitalia.com domain, with Reply-To set to the
// person who filled it in so answering is one click.
//
// Needs RESEND_API_KEY in the Vercel project's environment (a sending-only
// key for amamiitalia.com). Without it the handler answers
// { ok:false, fallback:true } and the browser opens a pre-filled email to
// info@ instead, so an enquiry is never lost while the key is missing.

const TO = 'info@amamiitalia.com';
const FROM = 'Amami Italia Website <website@amamiitalia.com>';

const SUBJECT = {
  event: 'Event enquiry',
  catering: 'Catering enquiry',
  contact: 'Contact form',
  careers: 'Careers application',
  'event-updates': 'Event alerts signup',
  newsletter: 'Newsletter signup',
};

const LABEL = {
  firstName: 'First name', lastName: 'Last name', name: 'Name', email: 'Email',
  phone: 'Phone', date: 'Date', guests: 'Guests', topic: 'About', role: 'Role',
  message: 'Message', page: 'Page',
};

const SKIP = new Set(['form', 'company_website']);
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const label = k => LABEL[k] || k.replace(/([a-z])([A-Z])/g, '$1 $2').replace(/^./, c => c.toUpperCase());

async function readBody(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  let raw = typeof req.body === 'string' ? req.body : '';
  if (!raw) for await (const chunk of req) raw += chunk;
  return Object.fromEntries(new URLSearchParams(raw));
}

function send(res, code, data) {
  res.statusCode = code;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.end(JSON.stringify(data));
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') return send(res, 405, { ok: false, error: 'POST only.' });

  let data;
  try { data = await readBody(req); } catch (e) { return send(res, 400, { ok: false }); }

  // Honeypot: a person never fills this in, a bot fills in everything.
  if (data.company_website) return send(res, 200, { ok: true });

  const email = String(data.email || '').trim();
  if (!EMAIL.test(email)) return send(res, 400, { ok: false, error: 'Please check your email address.' });

  const key = process.env.RESEND_API_KEY;
  if (!key) return send(res, 503, { ok: false, fallback: true });

  const type = String(data.form || 'contact').toLowerCase();
  const subject = SUBJECT[type] || 'Website form';
  const who = [data.firstName, data.lastName].filter(Boolean).join(' ') || data.name || email;

  // Fields in the order they were filled in, empty ones left out.
  const rows = Object.entries(data)
    .filter(([k, v]) => !SKIP.has(k) && String(v).trim() !== '')
    .map(([k, v]) => [label(k), String(v).trim().slice(0, 5000)]);

  const text = rows.map(([k, v]) => `${k}: ${v}`).join('\n');
  const html = '<table cellpadding="6" style="font-family:Arial,sans-serif;font-size:14px;border-collapse:collapse">' +
    rows.map(([k, v]) => `<tr><td style="color:#666;vertical-align:top;white-space:nowrap">${esc(k)}</td><td>${esc(v).replace(/\n/g, '<br>')}</td></tr>`).join('') +
    '</table>';

  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: 'Bearer ' + key, 'Content-Type': 'application/json' },
      body: JSON.stringify({ from: FROM, to: [TO], reply_to: email, subject: `${subject} — ${who}`, text, html }),
    });
    if (!r.ok) {
      console.error('resend', r.status, await r.text());
      return send(res, 502, { ok: false, fallback: true });
    }
    return send(res, 200, { ok: true });
  } catch (e) {
    console.error('resend', e);
    return send(res, 502, { ok: false, fallback: true });
  }
};
