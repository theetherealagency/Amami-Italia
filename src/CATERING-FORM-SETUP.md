# Catering enquiry form — backend setup

The form on `/catering-services/` posts to a Google Apps Script web app, which writes
each enquiry to a Google Sheet and emails you. Nothing runs on WordPress, so this keeps
working after `amamiitalia.com` moves to Vercel.

Takes about five minutes, once.

---

## 1. Make the sheet

1. Create a new Google Sheet named **Amami — Catering Enquiries**.
2. Leave it empty. The script writes the header row itself on the first submission.

## 2. Add the script

In that sheet: **Extensions → Apps Script**. Delete whatever is in `Code.gs` and paste
the contents of [`apps-script/catering-form.gs`](apps-script/catering-form.gs).

Set `NOTIFY_TO` at the top to whoever should get the emails. Separate several addresses
with commas.

## 3. Deploy it

1. **Deploy → New deployment**
2. Type: **Web app**
3. Description: `catering form`
4. Execute as: **Me**
5. Who has access: **Anyone** ← this matters; the form posts anonymously
6. **Deploy**, then authorise when Google asks (it will warn the app is unverified
   because you wrote it — choose **Advanced → Go to … (unsafe)**)
7. Copy the **Web app URL**. It ends in `/exec`.

## 4. Point the site at it

In `catering-services/index.html`, find:

```js
var ENDPOINT='__APPS_SCRIPT_URL__';
```

Replace the placeholder with your `/exec` URL, then redeploy:

```sh
vercel deploy --prod
```

Until you do this, the form deliberately refuses to submit and tells the visitor to
call instead — it never silently swallows an enquiry.

## 5. Check it

Submit a test enquiry from the live page. You should get a row in the sheet and an
email within a few seconds.

---

## Notes

**Why `mode: 'no-cors'`.** Apps Script does not return CORS headers on POST, so the
browser cannot read the response. The request still arrives. This means the page shows
"thank you" as soon as the request is sent rather than after the server confirms — so
keep an eye on the sheet for the first few days.

**Spam.** The form carries a hidden `company_website` field. Real people never fill it
in; bots usually do. The script drops any submission where it is populated.

**Changing the fields.** Add the input to the form in `catering-services/index.html`,
then add the same `name` to `FIELDS` in the script. The sheet picks up the new column
on the next submission.
