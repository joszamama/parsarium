<?php
declare(strict_types=1);
require __DIR__ . '/harness.php';

// The package API throws or returns no document on a rejected input; stop quietly for AFL++.
$path = $argv[1] ?? null;
if ($path === null || !is_file($path) || filesize($path) > (1 << 20)) { exit(0); }
$bytes = file_get_contents($path);
if ($bytes === false || $bytes === '') { exit(0); }
try { parsarium_parse($bytes); } catch (Throwable) { exit(0); }
