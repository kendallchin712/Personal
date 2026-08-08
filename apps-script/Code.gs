/**
 * Parrs Australia — Enquiry Form backend (Google Apps Script)
 * ----------------------------------------------------------------------------
 * Receives one lead per POST from paz-lead-form.html and appends it as a row
 * to the bound Google Sheet. Deploy this as a Web App (see SETUP.md).
 *
 * The form posts JSON as text/plain (no CORS preflight), so we read the raw
 * body from e.postData.contents and parse it ourselves.
 */

// Which tab to write to. It is created automatically if it doesn't exist.
var SHEET_NAME = 'Leads';

// Column order. The first column is a server-side timestamp we add on arrival;
// the rest mirror the fields sent by the form (and its CSV export).
var HEADERS = [
  'Received (server)',
  'Date',
  'Captured by',
  'Name',
  'Email',
  'Phone',
  'Store name',
  'Address',
  'Suburb',
  'State',
  'Postcode',
  'Rating',
  'Interested in / to discuss',
  'Submitted at (device)'
];

/**
 * Handle a lead submission.
 */
function doPost(e) {
  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(30000); // serialise writes so rows never collide

    var data = {};
    if (e && e.postData && e.postData.contents) {
      data = JSON.parse(e.postData.contents);
    } else if (e && e.parameter) {
      data = e.parameter; // fallback: form-encoded
    }

    var sheet = getSheet_();

    sheet.appendRow([
      new Date(),
      data.date || '',
      data.capturedBy || '',
      data.name || '',
      data.email || '',
      data.phone || '',
      data.store || '',
      data.address || '',
      data.suburb || '',
      data.state || '',
      data.postcode || '',
      data.rating || '',
      data.enquiry || '',
      data.submittedAt || ''
    ]);

    return json_({ ok: true });
  } catch (err) {
    return json_({ ok: false, error: String(err) });
  } finally {
    try { lock.releaseLock(); } catch (ignore) {}
  }
}

/**
 * A GET just returns a small health check so you can confirm the URL works in
 * a browser after deploying.
 */
function doGet() {
  return json_({ ok: true, service: 'Parrs enquiry form', time: new Date().toISOString() });
}

/**
 * Get (or create) the target sheet, ensuring the header row exists.
 */
function getSheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) sheet = ss.insertSheet(SHEET_NAME);
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(HEADERS);
    sheet.setFrozenRows(1);
    sheet.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold');
  }
  return sheet;
}

function json_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
