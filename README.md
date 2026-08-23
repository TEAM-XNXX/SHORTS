# Shortly — PHP/MySQL URL Shortener

## Requirements
- PHP 8.0+
- MySQL/MariaDB
- Apache with mod_rewrite (recommended)
- cPanel or another PHP hosting account

## Install
1. Create a MySQL database/user.
2. Import `db.sql`.
3. Open `config.php` and set `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASS`.
4. Change `ADMIN_USER` and `ADMIN_PASSWORD`.
5. Upload all files to your domain's public folder.
6. Make sure `.htaccess` is uploaded and Apache `mod_rewrite` is enabled.
7. Open `/index.php`.
8. Admin dashboard: `/admin.php`.

## Important
Set `BASE_URL` in `config.php` if the auto-detected URL is not correct, e.g.:
`const BASE_URL = 'https://example.com';`

For production, use HTTPS and a strong admin password. Do not leave the example password unchanged.
