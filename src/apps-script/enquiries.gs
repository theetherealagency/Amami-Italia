/**
 * Amami Italia — website form handler, bound to the sheet
 * "Amami Enquiries - Event" (docs.google.com/spreadsheets/d/19qSzznDcYxVcPPo4lwyPt4jozp6iUbbmxTv7sw0scIU).
 *
 * Every form on the site reaches this through the site's /api/forms/ function:
 * EVENT ENQUIRIES ONLY (/events/ and /it/events/):
 *   - added as a row on the first tab,
 *   - emailed to info@amamiitalia.com with every field,
 *   - and the guest gets a branded confirmation with a copy of what they sent
 *     (Reply-To info@, so their answer lands with the team).
 * Other forms on the site do not come here.
 * Emails and the sheet use the Amami brand book palette: Charcoal Black
 * #161616, Warm Beige #eee9da, Tuscan Brown #462e24, Medium Rare Red #812b28.
 *
 * Deploy (once): in the sheet, Extensions → Apps Script → paste this file over
 * Code.gs → Save → Deploy → New deployment → type "Web app" →
 * Execute as "Me" → Who has access "Anyone" → Deploy → allow the permissions
 * → copy the Web app URL (…/exec). The emails are sent from the Google account
 * that deploys it.
 */

var NOTIFY_TO = 'info@amamiitalia.com';
var SITE_NAME = 'Amami Italia';
var SITE_URL = 'https://amamiitalia.etherealpr.com';
// The logo travels inside the email (an inline cid: attachment), so it shows
// even in inboxes that block pictures from the web (Outlook / Microsoft 365
// do this for new senders). Baked onto charcoal, 300x243, 4 KB.
var LOGO_B64 = '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';
function logoBlob_() {
  return Utilities.newBlob(Utilities.base64Decode(LOGO_B64), 'image/png', 'amami-italia.png');
}

var BRAND = { ink: '#161616', beige: '#eee9da', brown: '#462e24', red: '#812b28', line: '#d9d2bf' };

var SUBJECT = {
  event: 'Event enquiry',
  catering: 'Catering enquiry',
  contact: 'Contact form',
  careers: 'Careers application',
  'event-updates': 'Event alerts signup'
};

// Columns of the Event sheet, in order. Anything else a form sends is folded
// into Message so nothing typed is ever lost.
var COLUMNS = ['received', 'space', 'firstName', 'lastName', 'email', 'phone', 'date', 'guests', 'message', 'page'];
var WIDTHS  = [150, 170, 120, 120, 220, 130, 110, 70, 360, 110];
// Every field of every form, in the order the guest fills them in. All of
// them appear in the team's email, even the ones left blank, so nothing the
// form asked is ever missing from the notification.
var FIELDS = {
  event:    ['space', 'firstName', 'lastName', 'email', 'phone', 'date', 'guests', 'message'],
  catering: ['firstName', 'lastName', 'email', 'phone', 'date', 'guests', 'message'],
  careers:  ['name', 'email', 'phone', 'role', 'message'],
  contact:  ['name', 'email', 'phone', 'topic', 'message'],
  'event-updates': ['email']
};
var FIELD_LABEL = {
  event:    { date: 'Event date', message: 'About the evening' },
  catering: { date: 'Date', message: 'What they are planning' }
};

var LABELS = {
  received: 'Received', firstName: 'First name', lastName: 'Last name', name: 'Name',
  email: 'Email', phone: 'Phone', date: 'Event date', guests: 'Guests', message: 'Message',
  page: 'Page', topic: 'About', role: 'Role', space: 'Space'
};

function doPost(e) {
  try {
    var data = parseBody_(e);
    if (data.company_website) return json_({ ok: true });            // honeypot
    if (!data.email) return json_({ ok: false, error: 'An email address is required.' });

    var type = String(data.form || 'contact').toLowerCase();
    // Events only (client, 2026-09-24): other forms are not handled here.
    if (type !== 'event') return json_({ ok: false, error: 'Only event enquiries are handled here.' });
    addRow_(data);
    notify_(type, data);
    try { confirmGuest_(type, data); } catch (x) { console.error('guest copy', x); }  // never fail the lead over this
    return json_({ ok: true });
  } catch (err) {
    return json_({ ok: false, error: String(err) });
  }
}

function doGet() {
  return json_({ ok: true, service: SITE_NAME + ' forms' });
}

/* ---- the sheet ---------------------------------------------------------- */

function addRow_(data) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  if (sheet.getLastRow() === 0) styleSheet_(sheet);
  else addSpaceColumn_(sheet);

  var extras = [];
  for (var k in data) {
    if (k === 'form' || k === 'company_website' || COLUMNS.indexOf(k) !== -1) continue;
    extras.push((LABELS[k] || k) + ': ' + data[k]);
  }
  var msg = [data.message || ''].concat(extras).filter(Boolean).join('\n');
  sheet.appendRow(COLUMNS.map(function (c) {
    if (c === 'received') return new Date();
    if (c === 'message') return msg;
    return data[c] || '';
  }));

  var r = sheet.getLastRow();
  var row = sheet.getRange(r, 1, 1, COLUMNS.length);
  row.setFontFamily('Poppins').setFontSize(10).setFontColor(BRAND.ink)
     .setVerticalAlignment('top').setWrap(true)
     .setBackground(r % 2 === 0 ? '#ffffff' : '#f6f3ea');
  sheet.getRange(r, 1).setNumberFormat('ddd d mmm yyyy, h:mm am/pm');
}

/* Brand the empty sheet once: charcoal header, beige serif labels, widths. */
function styleSheet_(sheet) {
  sheet.setName('Event Enquiries');
  sheet.appendRow(COLUMNS.map(function (c) { return LABELS[c] || c; }));
  var head = sheet.getRange(1, 1, 1, COLUMNS.length);
  head.setBackground(BRAND.ink).setFontColor(BRAND.beige)
      .setFontFamily('Cormorant Garamond').setFontSize(13).setFontWeight('bold')
      .setVerticalAlignment('middle');
  sheet.setRowHeight(1, 36);
  sheet.setFrozenRows(1);
  WIDTHS.forEach(function (w, i) { sheet.setColumnWidth(i + 1, w); });
  sheet.setTabColor(BRAND.red);
}

/* Sheets styled before the "Which space?" field existed have no Space
   column: add it after Received, styled like the rest of the header. */
function addSpaceColumn_(sheet) {
  if (String(sheet.getRange(1, 2).getValue()) === LABELS.space) return;
  sheet.insertColumnAfter(1);
  sheet.getRange(1, 2).setValue(LABELS.space)
       .setBackground(BRAND.ink).setFontColor(BRAND.beige)
       .setFontFamily('Cormorant Garamond').setFontSize(13).setFontWeight('bold').setVerticalAlignment('middle');
  sheet.setColumnWidth(2, 170);
}

/* Run this once from the editor (Run ▸ styleNow) to brand the sheet before
   the first enquiry arrives. Safe to run again. */
function styleNow() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  if (sheet.getLastRow() === 0) styleSheet_(sheet);
  else addSpaceColumn_(sheet);
}

/* ---- the emails --------------------------------------------------------- */

// The guest's copy is in the language of the page they wrote from.
var LABELS_IT = {
  space: 'Spazio', firstName: 'Nome', lastName: 'Cognome', name: 'Nome', email: 'Email',
  phone: 'Telefono', date: 'Data dell’evento', guests: 'Ospiti', message: 'La serata',
  role: 'Ruolo', topic: 'Argomento'
};
var SPACE_IT = {
  'The Private Room': 'La Sala Privata', 'The Lounge': 'Il Salotto',
  'The Long Table': 'Il Tavolo Lungo', 'Full Buyout': 'Uso esclusivo', 'Not sure yet': 'Non so ancora'
};
var DAYS_IT = ['domenica', 'lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato'];
var MONTHS_IT = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio',
                 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'];

function fieldRows_(type, data, lang) {
  var order = (FIELDS[type] || []).slice();
  for (var k in data) {                       // anything extra the form sent, after
    if (k === 'form' || k === 'company_website' || k === 'page' || order.indexOf(k) !== -1) continue;
    order.push(k);
  }
  return order.map(function (k) {
    var it = lang === 'it';
    var label = (it && LABELS_IT[k]) || (FIELD_LABEL[type] && FIELD_LABEL[type][k]) || LABELS[k] || k;
    var v = data[k] ? String(data[k]).trim() : '';
    if (k === 'date' && /^\d{4}-\d{2}-\d{2}$/.test(v)) {
      var d = new Date(v + 'T12:00:00');
      v = it ? DAYS_IT[d.getDay()] + ' ' + d.getDate() + ' ' + MONTHS_IT[d.getMonth()] + ' ' + d.getFullYear()
             : Utilities.formatDate(d, 'America/Toronto', 'EEEE d MMMM yyyy') + ' (' + v + ')';
    }
    if (k === 'space' && it && SPACE_IT[v]) v = SPACE_IT[v];
    return { key: k, label: label, value: v };
  });
}

function rowsHtml_(rows, linkify) {
  return rows.map(function (r) {
    var v = r.value;
    var cell = !v ? '<span style="color:#9a9384">&mdash; not given</span>'
      : linkify && r.key === 'email' ? '<a href="mailto:' + esc_(v) + '" style="color:' + BRAND.red + ';text-decoration:none">' + esc_(v) + '</a>'
      : linkify && r.key === 'phone' ? '<a href="tel:' + esc_(v.replace(/[^\d+]/g, '')) + '" style="color:' + BRAND.red + ';text-decoration:none">' + esc_(v) + '</a>'
      : esc_(v).replace(/\n/g, '<br>');
    return '<tr><td style="padding:10px 16px 10px 0;border-bottom:1px solid ' + BRAND.line + ';' +
      'font:11px/1.4 Arial,Helvetica,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:' + BRAND.brown + ';' +
      'vertical-align:top;white-space:nowrap">' + esc_(r.label) + '</td>' +
      '<td style="padding:10px 0;border-bottom:1px solid ' + BRAND.line + ';font:15px/1.5 Georgia,\'Times New Roman\',serif;color:' + BRAND.ink + '">' +
      cell + '</td></tr>';
  }).join('');
}

function shell_(inner) {
  return '<div style="margin:0;padding:24px 12px;background:' + BRAND.beige + '">' +
    '<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="max-width:600px;margin:0 auto;border-collapse:collapse">' +
    '<tr><td bgcolor="' + BRAND.ink + '" style="background:' + BRAND.ink + ';padding:18px 32px;text-align:center">' +
      '<a href="' + SITE_URL + '"><img src="cid:amamilogo" width="150" height="122" alt="Amami Italia" ' +
      'style="display:inline-block;width:150px;height:auto;border:0;background:' + BRAND.ink + '"></a>' +
    '</td></tr>' +
    '<tr><td bgcolor="#ffffff" style="background:#ffffff;padding:30px 32px 32px">' + inner + '</td></tr>' +
    '<tr><td bgcolor="' + BRAND.ink + '" style="background:' + BRAND.ink + ';padding:18px 32px;text-align:center;font:11px/1.7 Arial,Helvetica,sans-serif;letter-spacing:.14em;color:' + BRAND.beige + '">' +
      'AMAMI ITALIA &middot; 6261 MAYFIELD RD, #140, BRAMPTON, ON<br>' +
      '<a href="tel:+19057943366" style="color:' + BRAND.beige + ';text-decoration:none">905-794-3366</a> &middot; ' +
      '<a href="mailto:info@amamiitalia.com" style="color:' + BRAND.beige + ';text-decoration:none">INFO@AMAMIITALIA.COM</a>' +
    '</td></tr></table></div>';
}

function heading_(kicker, title, sub) {
  return '<p style="margin:0 0 6px;font:11px/1 Arial,Helvetica,sans-serif;letter-spacing:.22em;text-transform:uppercase;color:' + BRAND.red + '">' + kicker + '</p>' +
    '<h1 style="margin:0 0 4px;font:300 30px/1.15 \'Cormorant Garamond\',Georgia,\'Times New Roman\',serif;letter-spacing:.02em;text-transform:uppercase;color:' + BRAND.ink + '">' + esc_(title) + '</h1>' +
    (sub ? '<p style="margin:0 0 22px;font:italic 16px/1.4 Georgia,serif;color:' + BRAND.brown + '">' + esc_(sub) + '</p>' : '<div style="height:18px"></div>');
}

function notify_(type, data) {
  var title = SUBJECT[type] || 'Website form';
  var who = [data.firstName, data.lastName].filter(Boolean).join(' ') || data.name || data.email;
  var rows = fieldRows_(type, data);
  var when = Utilities.formatDate(new Date(), 'America/Toronto', 'EEE d MMM yyyy, h:mm a');
  var page = data.page ? SITE_URL + data.page : SITE_URL;
  var meta = [{ key: 'received', label: 'Received', value: when + ' (Toronto)' },
              { key: 'page', label: 'Sent from', value: page },
              { key: 'lang', label: 'Language', value: /^\/it\//.test(data.page || '') ? 'Italian' : 'English' }];

  var inner = heading_('New from the website', title, who) +
    '<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse;border-top:1px solid ' + BRAND.line + '">' +
      rowsHtml_(rows, true) + rowsHtml_(meta, false) + '</table>' +
    '<p style="margin:26px 0 0"><a href="mailto:' + esc_(data.email) + '?subject=' + encodeURIComponent('Re: ' + title + ' at Amami Italia') + '" ' +
      'style="display:inline-block;background:' + BRAND.red + ';color:' + BRAND.beige + ';font:12px/1 Arial,Helvetica,sans-serif;letter-spacing:.2em;text-transform:uppercase;text-decoration:none;padding:14px 26px">' +
      'Reply to ' + esc_(String(who).split(' ')[0]) + '</a></p>' +
    (type === 'event'
      ? '<p style="margin:22px 0 0;font:13px/1.5 Georgia,serif;font-style:italic;color:' + BRAND.brown + '">Also added to the <a href="' +
        SpreadsheetApp.getActiveSpreadsheet().getUrl() + '" style="color:' + BRAND.red + '">Amami Enquiries &ndash; Event</a> sheet.</p>' : '') +
    '<p style="margin:14px 0 0;font:12px/1.5 Arial,Helvetica,sans-serif;color:#8a8373">' + esc_(who) + ' has been sent a confirmation email with a copy of these details.</p>';

  var text = rows.concat(meta).map(function (r) { return r.label + ': ' + (r.value || '— not given'); }).join('\n');
  MailApp.sendEmail({
    to: NOTIFY_TO, replyTo: data.email, name: SITE_NAME + ' Website',
    subject: title + ' — ' + who,
    body: text + '\n\n— sent by the Amami Italia website',
    htmlBody: shell_(inner), inlineImages: { amamilogo: logoBlob_() }
  });
}

/* The guest's copy: a thank-you, what happens next, and exactly what they sent. */
var GUEST = {
  en: {
    event:    { subj: 'We have your event enquiry', h: 'Thank you', p: 'Your enquiry for an evening at Amami is with our events team. We answer within one business day, usually sooner, with the rooms that fit, menus and a quote.' },
    catering: { subj: 'We have your catering enquiry', h: 'Thank you', p: 'Your catering enquiry is with our team. We answer within one business day with menus and a quote.' },
    careers:  { subj: 'We have your application', h: 'Thank you', p: 'Thanks for wanting to work with us. The kitchen and floor managers read every application, and we will be in touch if there is a fit.' },
    contact:  { subj: 'We have your message', h: 'Thank you', p: 'Your message is with our team. We answer within one business day.' },
    'event-updates': { subj: 'You are on the list', h: 'You are on the list', p: 'We will write when there is something worth coming in for: tasting nights, holiday menus and events at Amami. Nothing more than that.' },
    copy: 'What you sent us', call: 'Need us sooner? Call', sign: 'A presto,<br>Amami Italia', book: 'Book a table'
  },
  it: {
    event:    { subj: 'Abbiamo ricevuto la tua richiesta per un evento', h: 'Grazie', p: 'La tua richiesta è arrivata al nostro team eventi. Rispondiamo entro un giorno lavorativo, di solito prima, con le sale adatte, i menù e un preventivo.' },
    catering: { subj: 'Abbiamo ricevuto la tua richiesta di catering', h: 'Grazie', p: 'La tua richiesta di catering è arrivata al nostro team. Rispondiamo entro un giorno lavorativo con menù e preventivo.' },
    careers:  { subj: 'Abbiamo ricevuto la tua candidatura', h: 'Grazie', p: 'Grazie per voler lavorare con noi. Leggiamo ogni candidatura e ti contatteremo se c’è l’occasione giusta.' },
    contact:  { subj: 'Abbiamo ricevuto il tuo messaggio', h: 'Grazie', p: 'Il tuo messaggio è arrivato al nostro team. Rispondiamo entro un giorno lavorativo.' },
    'event-updates': { subj: 'Sei nella lista', h: 'Sei nella lista', p: 'Ti scriveremo quando ci sarà qualcosa per cui vale la pena venire: serate di degustazione, menù delle feste ed eventi da Amami.' },
    copy: 'Cosa ci hai inviato', call: 'Serve prima? Chiama il', sign: 'A presto,<br>Amami Italia', book: 'Prenota un tavolo'
  }
};

function confirmGuest_(type, data) {
  var lang = /^\/it\//.test(data.page || '') ? 'it' : 'en';
  var L = GUEST[lang], c = L[type] || L.contact;
  var first = data.firstName || (data.name ? String(data.name).split(' ')[0] : '');
  var rows = fieldRows_(type, data, lang).filter(function (r) { return r.value; });
  var inner = heading_('Amami Italia', c.h + (first ? ', ' + first : ''), '') +
    '<p style="margin:0 0 22px;font:16px/1.6 Georgia,serif;color:' + BRAND.ink + '">' + esc_(c.p) + '</p>' +
    (type === 'event-updates' ? '' :
      '<p style="margin:0 0 8px;font:11px/1 Arial,Helvetica,sans-serif;letter-spacing:.2em;text-transform:uppercase;color:' + BRAND.brown + '">' + esc_(L.copy) + '</p>' +
      '<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse;border-top:1px solid ' + BRAND.line + '">' + rowsHtml_(rows, false) + '</table>') +
    '<p style="margin:24px 0 0;font:15px/1.6 Georgia,serif;color:' + BRAND.ink + '">' + esc_(L.call) +
      ' <a href="tel:+19057943366" style="color:' + BRAND.red + ';text-decoration:none">905-794-3366</a>.</p>' +
    '<p style="margin:18px 0 0;font:italic 16px/1.5 Georgia,serif;color:' + BRAND.brown + '">' + L.sign + '</p>' +
    '<p style="margin:26px 0 0"><a href="' + SITE_URL + (lang === 'it' ? '/it' : '') + '/reservation/" style="display:inline-block;border:1px solid ' + BRAND.red + ';color:' + BRAND.red + ';' +
      'font:12px/1 Arial,Helvetica,sans-serif;letter-spacing:.2em;text-transform:uppercase;text-decoration:none;padding:13px 24px">' + esc_(L.book) + '</a></p>';
  var text = c.p + '\n\n' + rows.map(function (r) { return r.label + ': ' + r.value; }).join('\n') +
    '\n\n' + L.call + ' 905-794-3366.\n\nAmami Italia\n6261 Mayfield Rd, #140, Brampton, ON';
  MailApp.sendEmail({
    to: data.email, replyTo: NOTIFY_TO, name: SITE_NAME,
    subject: c.subj + ' — Amami Italia',
    body: text, htmlBody: shell_(inner), inlineImages: { amamilogo: logoBlob_() }
  });
}

/* ---- plumbing ----------------------------------------------------------- */

function esc_(s) {
  return String(s).replace(/[&<>"']/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
  });
}

function parseBody_(e) {
  if (e && e.postData && e.postData.contents) {
    var raw = e.postData.contents;
    if (raw.charAt(0) === '{') { try { return JSON.parse(raw); } catch (x) {} }
  }
  return (e && e.parameter) ? e.parameter : {};
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
