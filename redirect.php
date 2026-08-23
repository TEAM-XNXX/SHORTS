<?php
require __DIR__.'/config.php';
$code = trim($_GET['code'] ?? '');
if (!preg_match('/^[A-Za-z0-9_-]{3,32}$/', $code)) { http_response_code(404); exit('Link not found'); }

$pdo = db();
$stmt = $pdo->prepare('SELECT id,long_url FROM links WHERE short_code=? LIMIT 1');
$stmt->execute([$code]);
$link = $stmt->fetch();

if (!$link) { http_response_code(404); exit('Link not found'); }

$pdo->prepare('UPDATE links SET clicks=clicks+1,last_clicked_at=NOW() WHERE id=?')->execute([$link['id']]);
header('Location: '.$link['long_url'], true, 302);
exit;
