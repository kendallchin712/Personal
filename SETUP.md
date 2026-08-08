# Parrs Australia Enquiry Form — Setup Guide

A digital replacement for the printed enquiry form. Fill it in on a tablet at the
stand, and every lead lands in a shared Google Sheet for follow-up. It also keeps a
copy on the device, so a dropped wifi connection never loses a lead.

**Files**
- `paz-lead-form.html` — the form itself (open this on the tablet).
- `apps-script/Code.gs` — the tiny backend that writes leads into the Google Sheet.
- `SETUP.md` — this guide.

You only do the setup below **once**, before the fair. It takes about 5 minutes.

---

## Part 1 — Create the Google Sheet + connect the backend

1. Go to **[sheets.new](https://sheets.new)** to create a new blank Google Sheet.
   Name it something like **"Parrs Leads — Melbourne Gift Fair"**.
2. In that Sheet's menu, click **Extensions → Apps Script**. A code editor opens in
   a new tab.
3. Delete whatever code is in the editor, then open `apps-script/Code.gs` from this
   project, **copy all of it**, and paste it in. Click the **Save** icon (💾).
4. Click **Deploy → New deployment**.
   - Click the gear ⚙️ next to "Select type" and choose **Web app**.
   - **Description:** anything, e.g. "Enquiry form".
   - **Execute as:** **Me**.
   - **Who has access:** **Anyone**. *(This lets the tablet send leads without anyone
     signing in. The URL is random and unguessable; only people you share it with can
     use it.)*
   - Click **Deploy**.
5. The first time, Google asks you to **authorise**. Click through:
   *Authorize access → choose your account → Advanced → Go to (project name) → Allow.*
6. Copy the **Web app URL** it shows you. It ends in **`/exec`**.
   *(Sanity check: paste it into a browser — you should see `{"ok":true,...}`.)*

## Part 2 — Connect the form to the Sheet

1. Open `paz-lead-form.html` in a text editor.
2. Near the bottom, find the **CONFIG** block:
   ```js
   const APPS_SCRIPT_URL = "";
   const STAFF = ["Joyce", "Kendall", "Other"];
   ```
3. Paste your Web app URL between the quotes for `APPS_SCRIPT_URL`, and edit `STAFF`
   to list whoever is manning the stand. For example:
   ```js
   const APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfy.../exec";
   const STAFF = ["Joyce", "Kendall", "Mei", "Other"];
   ```
4. Save the file. The orange "Setup needed" banner in the form disappears once the URL
   is set.

## Part 3 — Put the form on the tablet

Pick whichever is easiest:

- **Email/AirDrop it:** send `paz-lead-form.html` to the tablet and open it in Safari
  or Chrome.
- **From a USB/cloud drive:** open the file on the tablet's browser.

Then, for a clean full-screen, app-like experience:
- **iPad (Safari):** tap the **Share** icon → **Add to Home Screen**. A "Parrs
  Enquiry" icon appears; open it from there.
- **Android (Chrome):** menu **⋮ → Add to Home screen**.

---

## Using it at the stand

1. At the start of the day, set **Captured by** (top of the form) to whoever's holding
   the tablet — it's remembered for next time.
2. For each visitor: fill in the fields and tap **Save lead**. The form clears and is
   ready for the next person (Date and Captured by stay put).
3. **Name** plus **an email or phone** are required — everything else is optional.
4. The top bar shows how many leads you've captured and how many are **unsynced**.
   - If wifi drops, leads keep saving on the device and the "unsynced" count climbs.
   - When you're back online, tap **Sync now** (or it retries automatically) to push
     them to the Sheet.
5. **Export CSV** downloads every lead captured on that device — a handy end-of-day
   backup you can open in Excel or import anywhere.

## Good to know

- **Each tablet keeps its own local copy.** If you use more than one tablet, each has
  its own on-device list, but all of them write into the **same** Google Sheet.
- **Leads live in the browser's storage on that device.** Don't clear the browser's
  site data / history for this page before you've confirmed everything synced (or
  exported a CSV).
- **Privacy:** you're collecting people's contact details. Keep the Sheet shared only
  with the team who needs it, and handle the data per Parrs' normal privacy practices.

## Troubleshooting

- **Orange "Setup needed" banner still showing** → `APPS_SCRIPT_URL` isn't filled in
  (or the file wasn't saved / re-opened after editing).
- **Leads save but don't appear in the Sheet** → open the URL in a browser; if it
  doesn't return `{"ok":true}`, re-check the deployment (Part 1, steps 4–6). Make sure
  "Who has access" is **Anyone**.
- **Changed the Apps Script code later?** Re-deploy: **Deploy → Manage deployments →**
  edit ✏️ → **Version: New version → Deploy** (the `/exec` URL stays the same).
