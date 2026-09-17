/**
 * Amami Italia — one handler for every form on the site.
 *
 * Events, Catering, Contact and the footer newsletter all POST here. Each form
 * type gets its own tab in the spreadsheet, and a notification email goes out
 * with the fields laid out in the order they were filled in.
 *
 * Deploy: Extensions → Apps Script → paste this → Deploy → New deployment →
 * Web app → Execute as "Me" → Who has access "Anyone". See FORMS-SETUP.md.
 *
 * Supersedes catering-form.gs, which only handled the old /catering-services/
 * page and is kept in the repo for reference.
 */

var NOTIFY_TO = 'info@amamiitalia.com';   // comma-separate for several people
var SITE_NAME = 'Amami Italia';

/* One tab per form type. A type that is not listed here still gets stored —
   it lands in a tab named after itself — so a new form cannot silently drop
   enquiries on the floor. */
var TABS = {
  event:      { tab: 'Events',     subject: 'Event enquiry' },
  catering:   { tab: 'Catering',   subject: 'Catering enquiry' },
  contact:    { tab: 'Contact',    subject: 'Contact form' },
  newsletter: { tab: 'Newsletter', subject: 'Newsletter signup' }
};

/* Column order per tab. Anything posted that is not listed is appended to the
   Message column rather than thrown away. */
var COLUMNS = {
  Events:     ['received', 'firstName', 'lastName', 'email', 'phone', 'date', 'guests', 'message', 'page'],
  Catering:   ['received', 'firstName', 'lastName', 'email', 'phone', 'date', 'guests', 'message', 'page'],
  Contact:    ['received', 'topic', 'name', 'email', 'message', 'page'],
  Newsletter: ['received', 'email', 'page']
};

var LABELS = {
  received: 'Received', firstName: 'First name', lastName: 'Last name',
  email: 'Email', phone: 'Phone', date: 'Date', guests: 'Guests',
  message: 'Message', page: 'Page', topic: 'About', name: 'Name'
};

function doPost(e) {
  try {
    var data = parseBody_(e);

    // Honeypot. A real person never fills this in; a bot fills in everything.
    if (data.company_website) return json_({ ok: true });

    var type = String(data.form || 'contact').toLowerCase();
    var conf = TABS[type] || { tab: type.replace(/[^a-z0-9]/gi, '') || 'Other',
                               subject: 'Form submission' };

    if (!data.email) return json_({ ok: false, error: 'An email address is required.' });

    var sheet = getSheet_(conf.tab);
    var cols = COLUMNS[conf.tab] || Object.keys(data);
    var now = new Date();

    // Anything posted that has no column of its own is folded into Message, so
    // adding a field to a form never loses what people typed into it.
    var extras = [];
    for (var k in data) {
      if (k === 'form' || k === 'company_website') continue;
      if (cols.indexOf(k) === -1) extras.push((LABELS[k] || k) + ': ' + data[k]);
    }
    if (extras.length) {
      data.message = (data.message ? data.message + '\n\n' : '') + extras.join('\n');
    }

    var row = cols.map(function (c) { return c === 'received' ? now : (data[c] || ''); });
    sheet.appendRow(row);

    notify_(conf.subject, cols, row);
    return json_({ ok: true });
  } catch (err) {
    return json_({ ok: false, error: String(err) });
  }
}

function doGet() {
  return json_({ ok: true, service: SITE_NAME + ' forms' });
}

function parseBody_(e) {
  if (e && e.postData && e.postData.contents) {
    var raw = e.postData.contents;
    if (raw.charAt(0) === '{') { try { return JSON.parse(raw); } catch (x) {} }
  }
  return (e && e.parameter) ? e.parameter : {};
}

function getSheet_(name) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(name);
  if (!sheet) {
    sheet = ss.insertSheet(name);
    var cols = COLUMNS[name] || [];
    if (cols.length) {
      sheet.appendRow(cols.map(function (c) { return LABELS[c] || c; }));
      sheet.getRange(1, 1, 1, cols.length).setFontWeight('bold');
      sheet.setFrozenRows(1);
    }
  }
  return sheet;
}

function notify_(subject, cols, row) {
  if (!NOTIFY_TO) return;
  var lines = cols.map(function (c, i) {
    var v = row[i];
    if (!v) return null;
    return (LABELS[c] || c) + ': ' + (v instanceof Date ? v.toLocaleString() : v);
  }).filter(String);
  MailApp.sendEmail({
    to: NOTIFY_TO,
    subject: SITE_NAME + ' — ' + subject,
    body: lines.join('\n') + '\n\n— sent by the website',
    name: SITE_NAME
  });
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
