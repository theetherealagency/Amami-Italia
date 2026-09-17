/**
 * Amami Italia — catering enquiry handler.
 *
 * Receives POSTs from the form on /catering-services/, appends a row to this
 * spreadsheet and emails a notification.
 *
 * Deploy: Deploy → New deployment → Web app → Execute as "Me" → Access "Anyone".
 * See CATERING-FORM-SETUP.md in the repo.
 */

// Who gets notified. Comma-separate for several people.
var NOTIFY_TO = 'info@amamiitalia.com';

var SHEET_NAME = 'Enquiries';

// Column order in the sheet. Add to this if you add fields to the form.
var FIELDS = [
  'submitted_at', 'name', 'email', 'phone', 'event_type',
  'event_date', 'guests', 'location', 'message', 'page'
];

var HEADERS = [
  'Received', 'Name', 'Email', 'Phone', 'Event type',
  'Event date', 'Guests', 'Location', 'Message', 'Page'
];

function doPost(e) {
  try {
    var data = parseBody_(e);

    // honeypot — real visitors leave this empty
    if (data.company_website) {
      return json_({ ok: true, skipped: 'spam' });
    }

    if (!data.name || !data.email) {
      return json_({ ok: false, error: 'name and email are required' });
    }

    var sheet = getSheet_();
    var row = FIELDS.map(function (k) {
      if (k === 'submitted_at') {
        return data.submitted_at ? new Date(data.submitted_at) : new Date();
      }
      return data[k] || '';
    });
    sheet.appendRow(row);

    notify_(data);
    return json_({ ok: true });

  } catch (err) {
    // still record the failure so nothing is lost silently
    try {
      getSheet_().appendRow([new Date(), 'ERROR', String(err), '', '', '', '', '', '', '']);
    } catch (ignored) {}
    return json_({ ok: false, error: String(err) });
  }
}

function doGet() {
  return json_({ ok: true, service: 'amami catering form' });
}

/** Accepts JSON bodies and ordinary form posts. */
function parseBody_(e) {
  if (e && e.postData && e.postData.contents) {
    try {
      return JSON.parse(e.postData.contents);
    } catch (ignored) { /* fall through to form params */ }
  }
  var out = {};
  if (e && e.parameter) {
    Object.keys(e.parameter).forEach(function (k) { out[k] = e.parameter[k]; });
  }
  return out;
}

function getSheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
  }
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(HEADERS);
    sheet.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold');
    sheet.setFrozenRows(1);
  }
  return sheet;
}

function notify_(d) {
  if (!NOTIFY_TO) return;

  var subject = 'Catering enquiry — ' + (d.name || 'no name') +
                (d.event_date ? ' (' + d.event_date + ')' : '');

  var lines = [
    ['Name', d.name],
    ['Email', d.email],
    ['Phone', d.phone],
    ['Event type', d.event_type],
    ['Date', d.event_date],
    ['Guests', d.guests],
    ['Location', d.location],
    ['Message', d.message]
  ];

  var text = lines
    .filter(function (l) { return l[1]; })
    .map(function (l) { return l[0] + ': ' + l[1]; })
    .join('\n');

  var html = '<h2 style="font:600 18px system-ui;margin:0 0 14px">Catering enquiry</h2>' +
    '<table style="font:14px/1.6 system-ui;border-collapse:collapse">' +
    lines.filter(function (l) { return l[1]; }).map(function (l) {
      return '<tr>' +
        '<td style="padding:4px 14px 4px 0;color:#666;vertical-align:top">' + l[0] + '</td>' +
        '<td style="padding:4px 0">' + String(l[1]).replace(/\n/g, '<br>') + '</td>' +
        '</tr>';
    }).join('') +
    '</table>';

  MailApp.sendEmail({
    to: NOTIFY_TO,
    subject: subject,
    body: text,
    htmlBody: html,
    replyTo: d.email || undefined,
    name: 'Amami Italia website'
  });
}

function json_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
