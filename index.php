<?php
session_start();
require __DIR__.'/config.php';

$message = '';
$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    check_csrf();
    $url = trim($_POST['url'] ?? '');
    $custom = trim($_POST['custom'] ?? '');

    if (!valid_url($url)) {
        $error = 'Please enter a valid http:// or https:// URL.';
    } elseif ($custom !== '' && !preg_match('/^[A-Za-z0-9_-]{3,32}$/', $custom)) {
        $error = 'Custom code must be 3–32 characters: letters, numbers, _ or -.';
    } else {
        $pdo = db();
        if ($custom !== '') {
            $stmt = $pdo->prepare('SELECT id FROM links WHERE short_code=?');
            $stmt->execute([$custom]);
            if ($stmt->fetch()) $error = 'That custom code is already in use.';
            else $code = $custom;
        }
        if ($error === '') {
            if (!isset($code)) {
                do {
                    $code = random_code(6);
                    $stmt = $pdo->prepare('SELECT id FROM links WHERE short_code=?');
                    $stmt->execute([$code]);
                } while ($stmt->fetch());
            }
            $stmt = $pdo->prepare('INSERT INTO links(short_code,long_url) VALUES(?,?)');
            $stmt->execute([$code, $url]);
            $message = base_url().'/'.$code;
        }
    }
}
?>
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Shortly — URL Shortener</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<main class="hero">
  <div class="brand">SHORTLY<span>.</span></div>
  <h1>Make your links <em>shorter.</em></h1>
  <p class="sub">Fast, clean and self-hosted URL shortening with click tracking.</p>
  <section class="card">
    <form method="post">
      <input type="hidden" name="csrf" value="<?=htmlspecialchars(csrf_token())?>">
      <label>Long URL</label>
      <input name="url" type="url" placeholder="https://example.com/your/very/long/link" required>
      <label>Custom alias <small>(optional)</small></label>
      <div class="alias"><span><?=htmlspecialchars(parse_url(base_url(), PHP_URL_HOST) ?: 'example.com')?>/</span><input name="custom" maxlength="32" placeholder="my-link"></div>
      <button type="submit">Shorten URL →</button>
    </form>
    <?php if($error): ?><div class="alert error"><?=htmlspecialchars($error)?></div><?php endif; ?>
    <?php if($message): ?>
      <div class="result">
        <div><small>Your short link</small><a id="short" href="<?=htmlspecialchars($message)?>" target="_blank"><?=htmlspecialchars($message)?></a></div>
        <button class="copy" onclick="navigator.clipboard.writeText(document.getElementById('short').href);this.textContent='Copied!'">Copy</button>
      </div>
    <?php endif; ?>
  </section>
  <a class="admin-link" href="admin.php">Admin dashboard</a>
</main>
</body>
</html>
