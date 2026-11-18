# GoDaddy setup checklist: contact form (PHP + MySQL)

**Goal:** make the website contact form save every enquiry to a MySQL database and email it to
`hr@ndrinfotech.com` and `dineshreddyvari@ndrinfotech.com`.

**Estimated time:** 20 to 30 minutes.
**Status when this file was written:** the code is ready in `server/contact-api/` but is NOT live. Nothing on the website has been changed yet to use it (the live form still uses FormSubmit, which has been unreliable).

> Never write real passwords in this file or send them in chat. Keep the database password in a password manager.

---

## 0. What you need before you start

- [ ] GoDaddy account login (and access to the phone or email for the verification code)
- [ ] The project folder `E:\git_files\ndrinfotech_website` on your PC (the files are in `server\contact-api\`)
- [ ] A strong database password ready (at least 16 characters, letters, numbers and symbols)
- [ ] 30 minutes without interruption

---

## 1. Check the hosting server address

1. GoDaddy > **My Products** > **Domains** > `ndrinfotech.com` > **DNS**.
2. Find the `A` record named `admin` (or `mail`). Its value should be `132.148.183.180`.
3. [ ] Confirmed the address is `132.148.183.180`. If it is different, **use the different address** in step 2 and tell Claude.

## 2. Add the DNS record for the API

In the same DNS page click **Add New Record**:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | `api` | `132.148.183.180` | 600 seconds |

- [ ] Record saved. Do **not** change or delete any other record (especially `MX`, `TXT`, `CNAME` and the four `185.199.x.153` `A` records, which run your website and email).

## 3. Create the subdomain in cPanel

1. GoDaddy > **My Products** > **Web Hosting** > **Manage** > **cPanel Admin**.
2. Open **Domains** (or **Subdomains**).
3. Create `api.ndrinfotech.com` and set its document root to `api.ndrinfotech.com` (or `public_html/api`).

- [ ] Subdomain created. Folder name: `______________________`

## 4. Create the database and a restricted user

cPanel > **MySQL Databases**:

1. **Create New Database**: name `ndr` (cPanel adds a prefix, for example `abc123_ndr`).
2. **Add New User**: name `ndruser`, paste the strong password.
3. **Add User To Database**: choose the user and database, then in privileges tick **only** `SELECT` and `INSERT`.

- [ ] Full database name: `______________________`
- [ ] Full database user: `______________________`
- [ ] Password stored safely in a password manager

## 5. Create the table

cPanel > **phpMyAdmin** > click the database in the left list > **SQL** tab:

1. Open `server\contact-api\schema.sql` on your PC, copy everything.
2. Paste into the SQL box and click **Go**.

- [ ] Table `enquiries` now appears in the left list

## 6. Upload the files

cPanel > **File Manager** > open the subdomain folder from step 3. Click **Settings** (top right) and tick **Show Hidden Files (dotfiles)**.

Upload these from `server\contact-api\`:

- [ ] `contact.php`
- [ ] `.htaccess`
- [ ] `config.sample.php` then **rename it to `config.php`**

Edit `config.php` (right-click > Edit) and set:

- [ ] `db` > `name` = the full database name from step 4
- [ ] `db` > `user` = the full database user from step 4
- [ ] `db` > `pass` = your strong password
- [ ] `mail` > `to` = `hr@ndrinfotech.com` and `dineshreddyvari@ndrinfotech.com`
- [ ] `mail` > `from` = `no-reply@ndrinfotech.com` (must be an address on your own domain)
- [ ] `allowed_origins` keeps `https://www.ndrinfotech.com` and `https://ndrinfotech.com`

Do **not** upload `README.md`, `schema.sql` or `config.sample.php` after editing (the `.htaccess` blocks them, but keep the server tidy).

## 7. Turn on HTTPS for the API

cPanel > **SSL/TLS Status**:

1. Tick `api.ndrinfotech.com`.
2. Click **Run AutoSSL**.
3. Wait up to 10 minutes. The row should show a green padlock.

- [ ] Certificate issued

## 8. Test the API

On your PC open a terminal (PowerShell or Command Prompt) and run:

```bash
curl -i -X POST https://api.ndrinfotech.com/contact.php -H "Origin: https://www.ndrinfotech.com" -H "Content-Type: application/json" -d "{\"name\":\"Test\",\"email\":\"you@example.com\",\"phone\":\"9876543210\",\"topic\":\"Other\",\"msg\":\"API test\"}"
```

Expected results:

- [ ] The reply contains `{"ok":true}`
- [ ] A new row appears in phpMyAdmin > `enquiries` > **Browse**
- [ ] An email arrives in `hr@ndrinfotech.com` (check spam too)
- [ ] An email arrives in `dineshreddyvari@ndrinfotech.com` (check spam too)

If it fails, copy the full curl output and send it to Claude. Common causes:

| Symptom | Likely cause |
|---------|--------------|
| Could not resolve host | DNS record not added yet, wait up to an hour |
| Certificate error | AutoSSL has not finished, run it again |
| `{"ok":false,"error":"forbidden_origin"}` | The Origin in `allowed_origins` is wrong |
| `server_error` | Wrong database name, user or password in `config.php` |
| Row saved but no email | Check spam, and that `from` is an address on your domain |

## 9. Tell Claude it works

Send Claude: "API test passed" together with the curl output (nothing secret is in it).

---

## What Claude will do next (after step 9)

- [ ] Push the website change so the live form posts to `https://api.ndrinfotech.com/contact.php`
- [ ] Add a line to the Privacy Policy about saving enquiries
- [ ] Verify the live form end to end
- [ ] Optionally cut release `v1.1.0`

## Things to keep in mind

- **Do not cancel your GoDaddy hosting plan.** The API, your email and your other websites (dtradeschool.com, ndredtech.com, blog.ndredtech.com) depend on it.
- **Backups:** GoDaddy > Hosting > **Backups > Manage**. Make sure the database is covered.
- **Personal data:** the table stores names, emails, phone numbers, messages and IP addresses. Decide how long to keep them and delete old rows from phpMyAdmin.
- **Viewing enquiries:** cPanel > phpMyAdmin > database > `enquiries` > **Browse**. Use **Export** for a spreadsheet. Change `status` to `contacted` or `closed` as you work through them.
- **Changing who receives enquiries:** edit `mail` > `to` in `config.php` on the server. No website change is needed.

## Backup option if GoDaddy is not possible

If the setup cannot be completed, the form can use **Web3Forms** instead: create two access keys at <https://web3forms.com> (one for `hr@ndrinfotech.com`, one for `dineshreddyvari@ndrinfotech.com`) and send both keys to Claude. This does not need GoDaddy but does not save enquiries to a database.
