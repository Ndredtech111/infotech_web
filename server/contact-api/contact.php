<?php
/**
 * NDR Infotech - contact form API
 *
 * Receives the website contact form (JSON), validates it, saves it to MySQL
 * and emails it to the company inboxes.
 *
 * Deploy to the subdomain folder on GoDaddy cPanel hosting (see README.md).
 * Requires PHP 7.4+ with PDO MySQL. Credentials live in config.php (NOT in git).
 */
declare(strict_types=1);

ini_set('display_errors', '0');          // never leak errors to visitors
error_reporting(E_ALL);

$config = require __DIR__ . '/config.php';

/* ---------- helpers ---------- */
function respond(int $status, array $body): void
{
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('X-Content-Type-Options: nosniff');
    header('Cache-Control: no-store');
    echo json_encode($body, JSON_UNESCAPED_UNICODE);
    exit;
}

function clean(string $v, int $max): string
{
    $v = str_replace("\0", '', $v);
    $v = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $v) ?? '';
    $v = trim($v);
    return mb_substr($v, 0, $max, 'UTF-8');
}

/** True if text contains a web link (email addresses are allowed). */
function has_link(string $v): bool
{
    $v = preg_replace('/[^\s@]+@[^\s@]+\.[^\s@]+/', ' ', $v) ?? $v;
    $re = '/(https?:\/\/|ftp:\/\/|www\.|<\s*a\b|href\s*=|\[url|\b[a-z0-9-]+\.(?:com|org|io|info|biz|xyz|ru|cn|top|site|online|link|click|shop|app|ly|tk|ml|ga|cf)\b|\b[a-z0-9-]+\.[a-z]{2,}\/\S*)/i';
    return (bool) preg_match($re, $v);
}

function header_safe(string $v): string
{
    return trim(str_replace(["\r", "\n", "%0a", "%0d"], ' ', $v));
}

/* ---------- CORS: only our own website may call this ---------- */
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
$allowed = $config['allowed_origins'];
if ($origin !== '' && in_array($origin, $allowed, true)) {
    header('Access-Control-Allow-Origin: ' . $origin);
    header('Vary: Origin');
    header('Access-Control-Allow-Methods: POST, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type');
    header('Access-Control-Max-Age: 600');
}

if (($_SERVER['REQUEST_METHOD'] ?? '') === 'OPTIONS') {
    http_response_code(204);
    exit;
}
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    respond(405, ['ok' => false, 'error' => 'method_not_allowed']);
}
if ($origin === '' || !in_array($origin, $allowed, true)) {
    respond(403, ['ok' => false, 'error' => 'forbidden_origin']);
}

/* ---------- read and validate input ---------- */
$raw = file_get_contents('php://input', false, null, 0, 20000);
$in = json_decode($raw ?: '', true);
if (!is_array($in)) {
    respond(400, ['ok' => false, 'error' => 'bad_request']);
}

// honeypot: real visitors leave this empty
if (!empty($in['_honey'])) {
    respond(200, ['ok' => true]);        // pretend success, drop silently
}

$name  = clean((string) ($in['name'] ?? ''), 80);
$email = clean((string) ($in['email'] ?? ''), 120);
$phone = clean((string) ($in['phone'] ?? ''), 20);
$topic = clean((string) ($in['topic'] ?? ''), 40);
$msg   = clean((string) ($in['msg'] ?? ''), 2000);

$topics = ['Cloud', 'Data & BI', 'Development', 'Migration', 'DevOps', 'IT Talent', 'Wealth Management', 'Other'];
$digits = preg_replace('/\D/', '', $phone) ?? '';

$errors = [];
if ($name === '')                                        $errors[] = 'name';
if (!filter_var($email, FILTER_VALIDATE_EMAIL))          $errors[] = 'email';
if (!preg_match('/^[+()\d\s-]+$/', $phone) || strlen($digits) < 7 || strlen($digits) > 15) $errors[] = 'phone';
if (!in_array($topic, $topics, true))                    $topic = 'Other';
if ($msg === '')                                         $errors[] = 'message';
if (has_link($name) || has_link($msg))                   $errors[] = 'links_not_allowed';
if ($errors) {
    respond(422, ['ok' => false, 'error' => 'validation', 'fields' => $errors]);
}

$ip = substr((string) ($_SERVER['REMOTE_ADDR'] ?? ''), 0, 45);
$ua = substr((string) ($_SERVER['HTTP_USER_AGENT'] ?? ''), 0, 255);

/* ---------- database: rate limit + save ---------- */
$pdo = null;
$saved = false;
try {
    $db = $config['db'];
    $pdo = new PDO(
        'mysql:host=' . $db['host'] . ';dbname=' . $db['name'] . ';charset=utf8mb4',
        $db['user'],
        $db['pass'],
        [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_EMULATE_PREPARES => false]
    );

    // at most 3 enquiries per 10 minutes and 10 per day from one address
    $q = $pdo->prepare('SELECT SUM(created_at > (NOW() - INTERVAL 10 MINUTE)) AS recent, COUNT(*) AS today
                        FROM enquiries WHERE ip = :ip AND created_at > (NOW() - INTERVAL 1 DAY)');
    $q->execute([':ip' => $ip]);
    $row = $q->fetch(PDO::FETCH_ASSOC) ?: ['recent' => 0, 'today' => 0];
    if ((int) $row['recent'] >= 3 || (int) $row['today'] >= 10) {
        respond(429, ['ok' => false, 'error' => 'too_many_requests']);
    }

    $ins = $pdo->prepare('INSERT INTO enquiries (name, email, phone, topic, message, ip, user_agent)
                          VALUES (:name, :email, :phone, :topic, :message, :ip, :ua)');
    $ins->execute([
        ':name' => $name, ':email' => $email, ':phone' => $phone, ':topic' => $topic,
        ':message' => $msg, ':ip' => $ip, ':ua' => $ua,
    ]);
    $saved = true;
} catch (Throwable $e) {
    error_log('[ndr-contact] db error: ' . $e->getMessage());
}

/* ---------- email ---------- */
$mail = $config['mail'];
$to = implode(', ', $mail['to']);
$subject = '=?UTF-8?B?' . base64_encode('Website enquiry - ' . $topic . ' - ' . header_safe($name)) . '?=';

$body = "New website enquiry\r\n"
      . "-------------------\r\n"
      . "Name:     {$name}\r\n"
      . "Email:    {$email}\r\n"
      . "Mobile:   {$phone}\r\n"
      . "Interest: {$topic}\r\n\r\n"
      . "Message:\r\n{$msg}\r\n\r\n"
      . "-------------------\r\n"
      . 'Received: ' . date('Y-m-d H:i:s') . " (server time)\r\n"
      . "IP: {$ip}\r\n";

$headers = [
    'From: NDR Infotech Website <' . $mail['from'] . '>',
    'Reply-To: ' . header_safe($name) . ' <' . header_safe($email) . '>',
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
    'X-Mailer: ndr-contact-api',
];

$sent = @mail($to, $subject, $body, implode("\r\n", $headers), '-f' . $mail['from']);
if (!$sent) {
    error_log('[ndr-contact] mail() failed');
}

if ($saved || $sent) {
    respond(200, ['ok' => true]);
}
respond(500, ['ok' => false, 'error' => 'server_error']);
