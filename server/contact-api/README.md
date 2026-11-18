# Contact API (PHP + MySQL)

Receives the website contact form, saves it to MySQL and emails the company inboxes.

```
Visitor  ->  www.ndrinfotech.com (GitHub Pages)  ->  api.ndrinfotech.com/contact.php (GoDaddy)  ->  MySQL + email
```

## Files

| File | Purpose |
|------|---------|
| `contact.php` | The API endpoint |
| `config.sample.php` | Template for the private settings. Copy to `config.php` on the server |
| `schema.sql` | Creates the `enquiries` table |
| `.htaccess` | Blocks access to private files and forces HTTPS |

`config.php` holds the database password and is **never committed to git**.

## One-time setup on GoDaddy

### 1. DNS (GoDaddy > Domains > ndrinfotech.com > DNS)
Add an **A record**: Name `api`, Value `132.148.183.180` (your hosting server's address, the same one used by your `admin` and `mail` records), TTL 600.

### 2. Subdomain (hosting > cPanel Admin > Domains)
Create the subdomain `api.ndrinfotech.com`. Set the document root to `api.ndrinfotech.com` (or `public_html/api`).

### 3. Database (cPanel > MySQL Databases)
1. Create a database, for example `ndr` (cPanel adds your account prefix, e.g. `abc123_ndr`).
2. Create a database user with a **strong password**.
3. **Add the user to the database** with these privileges only: `SELECT`, `INSERT`.

### 4. Create the table (cPanel > phpMyAdmin)
Open the database, click the **SQL** tab, paste the contents of `schema.sql` and click **Go**.

### 5. Upload the files (cPanel > File Manager)
Open the subdomain folder and upload `contact.php` and `.htaccess`
(enable "Show hidden files" to see `.htaccess`).
Upload `config.sample.php`, rename it to `config.php` and edit it with the real database name, user and password.

### 6. HTTPS (cPanel > SSL/TLS Status)
Select `api.ndrinfotech.com` and click **Run AutoSSL**. Wait a few minutes until it shows a certificate.

### 7. Test
From any computer:

```bash
curl -i -X POST https://api.ndrinfotech.com/contact.php \
  -H "Origin: https://www.ndrinfotech.com" -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"you@example.com","phone":"9876543210","topic":"Other","msg":"API test"}'
```

Expected: `{"ok":true}`, a new row in phpMyAdmin (`enquiries` table) and an email in both inboxes.

## Viewing enquiries
cPanel > phpMyAdmin > your database > `enquiries` table > **Browse**. Use **Export** to download a spreadsheet. Change the `status` column to `contacted` or `closed` as you work through them.

## Protection built in
- Only `https://www.ndrinfotech.com` and `https://ndrinfotech.com` may call the API (CORS and Origin check)
- Input validation, no web links in name or message, length limits
- Hidden trap field for bots
- Rate limit per IP address: 3 per 10 minutes and 10 per day
- Database writes use prepared statements (no SQL injection)
- The database user can only `SELECT` and `INSERT`
- Enquiries are saved first, then emailed, so none are lost if email fails

## Privacy
Enquiries contain personal data (name, email, phone, message, IP address). Mention this in the Privacy Policy and delete old rows when they are no longer needed.

## Changing recipients
Edit the `mail.to` list in `config.php` on the server. No website change is needed.
