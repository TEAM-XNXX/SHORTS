<?php
session_start();
require __DIR__.'/config.php';

if (isset($_GET['logout'])) { session_destroy(); header('Location: admin.php'); exit; }

if (!admin_logged_in()) {
    $err='';
    if ($_SERVER['REQUEST_METHOD']==='POST') {
        check_csrf();
        if (hash_equals(ADMIN_USER, $_POST['username'] ?? '') && hash_equals(ADMIN_PASSWORD, $_POST['password'] ?? '')) {
            session_regenerate_id(true); $_SESSION['admin']=true; header('Location: admin.php'); exit;
        }
        $err='Invalid username or password.';
    }
    ?>
    <!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Admin Login</title><link rel="stylesheet" href="assets/style.css"></head>
    <body><main class="login"><div class="brand">SHORTLY<span>.</span></div><section class="card"><h2>Admin Login</h2><?php if($err):?><div class="alert error"><?=$err?></div><?php endif;?><form method="post"><input type="hidden" name="csrf" value="<?=htmlspecialchars(csrf_token())?>"><label>Username</label><input name="username" required><label>Password</label><input type="password" name="password" required><button>Sign in</button></form></section></main></body></html>
    <?php exit;
}

$pdo=db();
if ($_SERVER['REQUEST_METHOD']==='POST') {
    check_csrf();
    if (isset($_POST['delete'])) {
        $pdo->prepare('DELETE FROM links WHERE id=?')->execute([(int)$_POST['delete']]);
    }
    header('Location: admin.php'); exit;
}
$stats = [
 'links'=>(int)$pdo->query('SELECT COUNT(*) FROM links')->fetchColumn(),
 'clicks'=>(int)$pdo->query('SELECT COALESCE(SUM(clicks),0) FROM links')->fetchColumn(),
 'today'=>(int)$pdo->query('SELECT COUNT(*) FROM links WHERE created_at >= CURDATE()')->fetchColumn(),
];
$rows=$pdo->query('SELECT * FROM links ORDER BY id DESC LIMIT 200')->fetchAll();
?>
<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Dashboard — Shortly</title><link rel="stylesheet" href="assets/style.css"></head>
<body><div class="dash">
<header><div class="brand">SHORTLY<span>.</span></div><nav><a href="index.php">Create link</a><a href="?logout=1">Logout</a></nav></header>
<h1>Dashboard</h1>
<div class="stats"><div><b><?=$stats['links']?></b><span>Total links</span></div><div><b><?=$stats['clicks']?></b><span>Total clicks</span></div><div><b><?=$stats['today']?></b><span>Created today</span></div></div>
<section class="table-card"><div class="table-wrap"><table><thead><tr><th>Short URL</th><th>Destination</th><th>Clicks</th><th>Created</th><th></th></tr></thead><tbody>
<?php foreach($rows as $r): ?><tr><td><a target="_blank" href="<?=htmlspecialchars(base_url().'/'.$r['short_code'])?>"><?=htmlspecialchars($r['short_code'])?></a></td><td class="url"><?=htmlspecialchars($r['long_url'])?></td><td><?=$r['clicks']?></td><td><?=htmlspecialchars($r['created_at'])?></td><td><form method="post" onsubmit="return confirm('Delete this link?')"><input type="hidden" name="csrf" value="<?=htmlspecialchars(csrf_token())?>"><button class="danger" name="delete" value="<?=$r['id']?>">Delete</button></form></td></tr><?php endforeach; ?>
</tbody></table></div></section>
</div></body></html>
