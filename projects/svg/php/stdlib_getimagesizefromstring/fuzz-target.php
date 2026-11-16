<?php
declare(strict_types=1);

$path = $argv[1] ?? null;
if ($path === null || !is_file($path) || filesize($path) > (1 << 20)) { exit(0); }
$bytes = file_get_contents($path);
if ($bytes !== false) { @getimagesizefromstring($bytes); }
