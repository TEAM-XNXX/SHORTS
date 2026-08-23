<?php
declare(strict_types=1);

const DB_HOST = 'localhost';
const DB_NAME = 'shortener';
const DB_USER = 'root';
const DB_PASS = '';
const BASE_URL = ''; // e.g. https://example.com

const ADMIN_USER = 'admin';
const ADMIN_PASSWORD = 'change-this-password';

function db(): PDO {
    static $pdo = null;
    if ($pdo instanceof PDO) return $pdo;
    $dsn = 'mysql:host='.DB_HOST.';dbname='.DB_NAME.';charset=utf8mb4';
    $pdo = new PDO($dsn, DB_USER, DB_PASS, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES => false,
    ]);
    return $pdo;
}

function base_url(): string {
    if (BASE_URL !== '') return rtrim(BASE_URL, '/');
    $https = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') || (($_SERVER['SERVER_PORT'] ?? '') === '443');
    $scheme = $https ? 'https' : 'http';
    $host = $_SERVER['HTTP_HOST'] ?? 'localhost';
    $dir = rtrim(str_replace('\\','/', dirname($_SERVER['SCRIPT_NAME'] ?? '/')), '/');
    return $scheme.'://'.$host.($dir === '/' ? '' : $dir);
}

function random_code(int $length = 6): string {
    $chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    $out = '';
    for ($i=0; $i<$length; $i++) $out .= $chars[random_int(0, strlen($chars)-1)];
    return $out;
}

function valid_url(string $url): bool {
    return filter_var($url, FILTER_VALIDATE_URL) && preg_match('~^https?://~i', $url);
}

function csrf_token(): string {
    if (empty($_SESSION['csrf'])) $_SESSION['csrf'] = bin2hex(random_bytes(32));
    return $_SESSION['csrf'];
}

function check_csrf(): void {
    if (!hash_equals($_SESSION['csrf'] ?? '', $_POST['csrf'] ?? '')) {
        http_response_code(419); exit('Invalid CSRF token');
    }
}

function admin_logged_in(): bool {
    return !empty($_SESSION['admin']);
}
