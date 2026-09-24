// Every form on the site posts here: POST /api/forms/ (urlencoded, from
// amami.js).
//
// 1. SCRIPT_URL set: the submission is forwarded to the Apps Script web app
//    bound to the "Amami Enquiries - Event" Google Sheet
//    (apps-script/enquiries.gs). It adds event enquiries to the sheet and
//    emails every form to info@amamiitalia.com.
// 2. Otherwise, RESEND_API_KEY set: emailed to info@ through Resend from the
//    verified amamiitalia.com domain.
// 3. Neither: answers { ok:false, fallback:true } and the browser opens a
//    pre-filled email to info@, so an enquiry is never lost.

// The Apps Script web app URL (…/exec). Not a secret: it only accepts posts.
const SCRIPT_URL = process.env.FORMS_SCRIPT_URL || '';

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

  if (SCRIPT_URL) {
    try {
      const body = new URLSearchParams();
      for (const [k, v] of Object.entries(data)) body.append(k, String(v).slice(0, 5000));
      // Apps Script answers a POST with a 302 to its echo URL; fetch follows it.
      const r = await fetch(SCRIPT_URL, { method: 'POST', body, redirect: 'follow' });
      const d = await r.json().catch(() => null);
      if (d && d.ok) return send(res, 200, { ok: true });
      console.error('apps-script', r.status, d);
    } catch (e) {
      console.error('apps-script', e);
    }
    // fall through to Resend, then to the browser's email fallback
  }

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
