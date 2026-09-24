/**
 * Amami Italia — website form handler, bound to the sheet
 * "Amami Enquiries - Event" (docs.google.com/spreadsheets/d/19qSzznDcYxVcPPo4lwyPt4jozp6iUbbmxTv7sw0scIU).
 *
 * Every form on the site reaches this through the site's /api/forms/ function:
 *   - Event enquiries (/events/) are added as a row on the first tab, and
 *     emailed to info@amamiitalia.com.
 *   - Every other form (catering, careers, event alerts) is emailed to info@
 *     only, so the Event sheet holds nothing but event leads.
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
var LOGO = SITE_URL + '/wp-content/uploads/2025/09/amami-logo-300x278.png';

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
var COLUMNS = ['received', 'firstName', 'lastName', 'email', 'phone', 'date', 'guests', 'message', 'page'];
var WIDTHS  = [150, 120, 120, 220, 130, 110, 70, 360, 110];
var LABELS = {
  received: 'Received', firstName: 'First name', lastName: 'Last name', name: 'Name',
  email: 'Email', phone: 'Phone', date: 'Event date', guests: 'Guests', message: 'Message',
  page: 'Page', topic: 'About', role: 'Role'
};

function doPost(e) {
  try {
    var data = parseBody_(e);
    if (data.company_website) return json_({ ok: true });            // honeypot
    if (!data.email) return json_({ ok: false, error: 'An email address is required.' });

    var type = String(data.form || 'contact').toLowerCase();
    if (type === 'event') addRow_(data);
    notify_(type, data);
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

/* Run this once from the editor (Run ▸ styleNow) to brand the sheet before
   the first enquiry arrives. Safe to run again. */
function styleNow() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  if (sheet.getLastRow() === 0) styleSheet_(sheet);
}

/* ---- the email ---------------------------------------------------------- */

function notify_(type, data) {
  var title = SUBJECT[type] || 'Website form';
  var who = [data.firstName, data.lastName].filter(Boolean).join(' ') || data.name || data.email;

  var rows = [], text = [];
  for (var k in data) {
    if (k === 'form' || k === 'company_website' || !data[k]) continue;
    var label = LABELS[k] || k, val = String(data[k]);
    text.push(label + ': ' + val);
    rows.push(
      '<tr><td style="padding:10px 16px 10px 0;border-bottom:1px solid ' + BRAND.line + ';' +
      'font:11px/1.4 Arial,Helvetica,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:' + BRAND.brown + ';' +
      'vertical-align:top;white-space:nowrap">' + esc_(label) + '</td>' +
      '<td style="padding:10px 0;border-bottom:1px solid ' + BRAND.line + ';font:15px/1.5 Georgia,\'Times New Roman\',serif;color:' + BRAND.ink + '">' +
      (k === 'email' ? '<a href="mailto:' + esc_(val) + '" style="color:' + BRAND.red + ';text-decoration:none">' + esc_(val) + '</a>'
       : k === 'phone' ? '<a href="tel:' + esc_(val.replace(/[^\d+]/g, '')) + '" style="color:' + BRAND.red + ';text-decoration:none">' + esc_(val) + '</a>'
       : esc_(val).replace(/\n/g, '<br>')) +
      '</td></tr>');
  }
  var sheetNote = type === 'event'
    ? '<p style="margin:22px 0 0;font:13px/1.5 Georgia,serif;font-style:italic;color:' + BRAND.brown + '">' +
      'Also added to the <a href="' + SpreadsheetApp.getActiveSpreadsheet().getUrl() + '" style="color:' + BRAND.red + '">Amami Enquiries &ndash; Event</a> sheet.</p>'
    : '';

  var html =
    '<div style="margin:0;padding:24px 12px;background:' + BRAND.beige + '">' +
    '<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="max-width:600px;margin:0 auto;border-collapse:collapse">' +
    '<tr><td style="background:' + BRAND.ink + ';padding:26px 32px;text-align:center">' +
      '<img src="' + LOGO + '" width="96" alt="Amami Italia" style="display:inline-block;width:96px;height:auto;border:0">' +
    '</td></tr>' +
    '<tr><td style="background:#ffffff;padding:30px 32px 32px">' +
      '<p style="margin:0 0 6px;font:11px/1 Arial,Helvetica,sans-serif;letter-spacing:.22em;text-transform:uppercase;color:' + BRAND.red + '">New from the website</p>' +
      '<h1 style="margin:0 0 4px;font:300 30px/1.15 \'Cormorant Garamond\',Georgia,\'Times New Roman\',serif;letter-spacing:.02em;text-transform:uppercase;color:' + BRAND.ink + '">' + esc_(title) + '</h1>' +
      '<p style="margin:0 0 22px;font:italic 16px/1.4 Georgia,serif;color:' + BRAND.brown + '">' + esc_(who) + '</p>' +
      '<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse;border-top:1px solid ' + BRAND.line + '">' + rows.join('') + '</table>' +
      '<p style="margin:26px 0 0"><a href="mailto:' + esc_(data.email) + '" style="display:inline-block;background:' + BRAND.red + ';color:' + BRAND.beige + ';' +
      'font:12px/1 Arial,Helvetica,sans-serif;letter-spacing:.2em;text-transform:uppercase;text-decoration:none;padding:14px 26px">Reply to ' + esc_(who.split(' ')[0]) + '</a></p>' +
      sheetNote +
    '</td></tr>' +
    '<tr><td style="background:' + BRAND.ink + ';padding:18px 32px;text-align:center;font:11px/1.6 Arial,Helvetica,sans-serif;letter-spacing:.14em;color:' + BRAND.beige + '">' +
      'AMAMI ITALIA &middot; 6261 MAYFIELD RD, #140, BRAMPTON &middot; 905-794-3366' +
    '</td></tr></table></div>';

  MailApp.sendEmail({
    to: NOTIFY_TO,
    replyTo: data.email,
    name: SITE_NAME + ' Website',
    subject: title + ' — ' + who,
    body: text.join('\n') + '\n\n— sent by the Amami Italia website',
    htmlBody: html
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
