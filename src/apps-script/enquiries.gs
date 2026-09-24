/**
 * Amami Italia — website form handler, bound to the sheet
 * "Amami Enquiries - Event" (docs.google.com/spreadsheets/d/19qSzznDcYxVcPPo4lwyPt4jozp6iUbbmxTv7sw0scIU).
 *
 * Every form on the site reaches this through the site's /api/forms/ function:
 *   - Event enquiries (/events/) are added as a row on the first tab, and
 *     emailed to info@amamiitalia.com.
 *   - Every other form (catering, careers, event alerts) is emailed to info@
 *     only, so the Event sheet holds nothing but event leads.
 *
 * Deploy (once): in the sheet, Extensions → Apps Script → paste this file over
 * Code.gs → Save → Deploy → New deployment → type "Web app" →
 * Execute as "Me" → Who has access "Anyone" → Deploy → allow the permissions
 * → copy the Web app URL (…/exec). The emails are sent from the Google account
 * that deploys it.
 */

var NOTIFY_TO = 'info@amamiitalia.com';
var SITE_NAME = 'Amami Italia';

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
var LABELS = {
  received: 'Received', firstName: 'First name', lastName: 'Last name', name: 'Name',
  email: 'Email', phone: 'Phone', date: 'Date', guests: 'Guests', message: 'Message',
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

function addRow_(data) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(COLUMNS.map(function (c) { return LABELS[c] || c; }));
    sheet.getRange(1, 1, 1, COLUMNS.length).setFontWeight('bold');
    sheet.setFrozenRows(1);
  }
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
}

function notify_(type, data) {
  var who = [data.firstName, data.lastName].filter(Boolean).join(' ') || data.name || data.email;
  var lines = [];
  for (var k in data) {
    if (k === 'form' || k === 'company_website' || !data[k]) continue;
    lines.push((LABELS[k] || k) + ': ' + data[k]);
  }
  MailApp.sendEmail({
    to: NOTIFY_TO,
    replyTo: data.email,
    name: SITE_NAME + ' Website',
    subject: (SUBJECT[type] || 'Website form') + ' — ' + who,
    body: lines.join('\n') + (type === 'event'
      ? '\n\nAlso added to the "Amami Enquiries - Event" sheet.' : '') + '\n\n— sent by the website'
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
