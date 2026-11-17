<?php
declare(strict_types=1);

// Parse-time target: DOMDocument::loadXML builds the tree in libxml2 (parser.c, SAX2.c) and ext/dom
// document.c; no adapter traversal runs, so AFL++ feedback comes from parsing the input bytes.
$path = $argv[1] ?? null;
if ($path === null || !is_file($path) || filesize($path) > (1 << 20)) { exit(0); }
$bytes = file_get_contents($path);
if ($bytes === false || $bytes === '') { exit(0); }
libxml_use_internal_errors(true);
(new DOMDocument())->loadXML($bytes, LIBXML_NONET);
