<?php
declare(strict_types=1);
require __DIR__ . '/summary.php';

// Parse-time target: ext/xml has no tree, so the same event handlers that build the summary run inside
// xml_parse (libxml2 push parser via ext/xml/compat.c); only the JSON output step of harness.php is skipped.
$path = $argv[1] ?? null;
if ($path === null || !is_file($path) || filesize($path) > (1 << 20)) { exit(0); }
$bytes = file_get_contents($path);
if ($bytes === false || $bytes === '') { exit(0); }
try {
    parsarium_xml_parse($bytes);
} catch (RuntimeException) {
}
