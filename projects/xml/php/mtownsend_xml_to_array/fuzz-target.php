<?php
declare(strict_types=1);
require __DIR__ . '/harness.php';

// XmlToArray::convert throws no documented exception; libxml2 errors surface as PHP warnings.
$path = $argv[1] ?? null;
if ($path === null || !is_file($path) || filesize($path) > (1 << 20)) { exit(0); }
$bytes = file_get_contents($path);
if ($bytes === false || $bytes === '') { exit(0); }
parsarium_parse($bytes);
