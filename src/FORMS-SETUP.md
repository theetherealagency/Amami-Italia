# Site forms — backend setup

Every form on the site posts to one Google Apps Script web app, which writes the
enquiry to a Google Sheet and emails it. Nothing runs on WordPress, so this keeps
working wherever the site is hosted.

Four forms feed it:

| Form | Page | Sheet tab |
|---|---|---|
| Event enquiry | `/events/#enquiry` | Events |
| Catering enquiry | `/catering/#enquiry` | Catering |
| Contact | `/visit/contact/` | Contact |
| Newsletter | site footer | Newsletter |

**Until this is set up, the forms open a pre-filled email to info@amamiitalia.com
instead of posting.** Enquiries still reach somebody; they just don't land in a sheet.

Takes about five minutes, once.

---

## 1. Make the sheet

Create a Google Sheet named **Amami Italia — Website enquiries**. Leave it empty;
the script creates each tab and its header row the first time that form is used.

## 2. Add the script

In that sheet: **Extensions → Apps Script**. Delete whatever is in `Code.gs` and
paste the contents of [`apps-script/forms.gs`](apps-script/forms.gs).

At the top, set `NOTIFY_TO` to whoever should get the emails. Comma-separate several
addresses.

## 3. Deploy it

1. **Deploy → New deployment**
2. Type: **Web app**
3. Execute as: **Me**
4. Who has access: **Anyone** ← this matters. The forms post anonymously; with
   "Anyone with a Google account" every submission fails.
5. **Deploy**, approve the permissions prompt, and copy the **Web app URL**. It
   looks like `https://script.google.com/macros/s/AKfycb…/exec`.

## 4. Put the URL in the build

In `tools/build_structure.py`, near the top:

```python
FORMS_ENDPOINT = "https://script.google.com/macros/s/AKfycb…/exec"
```

Then rebuild and deploy:

```
python3 tools/build_structure.py
vercel --prod --scope the-ethereal-agency
```

## 5. Check it

Submit the contact form on the live site. A row should appear in the **Contact**
tab within a few seconds and an email should arrive. If nothing happens, open the
browser console — the script reports its own errors in the response.

---

## Notes

- **Re-deploying the script**: after editing `forms.gs`, use **Deploy → Manage
  deployments → edit → Version: New version**. Creating a *new deployment* gives
  you a different URL and the site keeps posting to the old one.
- **Spam**: each form carries a hidden `company_website` field. Bots fill it in,
  people don't; anything that fills it is accepted and silently dropped.
- **New fields**: add the input to the form in the generator and the column name
  to `COLUMNS` in `forms.gs`. A field with no column is not lost — it gets appended
  to the Message column.
- `apps-script/catering-form.gs` is the older single-purpose version, kept for
  reference. `forms.gs` supersedes it.
