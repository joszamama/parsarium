<?php
declare(strict_types=1);
require __DIR__ . '/harness.php';

// Parse-time target: XML_Parser builds no tree, so the same handler object that builds the summary runs inside
// XML_Parser::parse() (xml_parse over the libxml2 push parser via ext/xml/compat.c); only the JSON output is skipped.
$path = $argv[1] ?? null;
if ($path === null || !is_file($path) || filesize($path) > (1 << 20)) { exit(0); }
$bytes = file_get_contents($path);
if ($bytes === false || $bytes === '') { exit(0); }
try {
    parsarium_parse($bytes);
} catch (RuntimeException) {
    // XML_Parser returns a PEAR error for rejected input, which the summary turns into RuntimeException.
}
