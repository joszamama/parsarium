<?php
declare(strict_types=1);

$path = $argv[1] ?? null;
if ($path === null || !is_file($path) || filesize($path) > (1 << 20)) { exit(0); }
$bytes = file_get_contents($path);
if ($bytes === false || $bytes === '') { exit(0); }
libxml_use_internal_errors(true);
$reader = XMLReader::XML($bytes, null, LIBXML_NONET);
while ($reader->read()) {
    if ($reader->nodeType === XMLReader::ELEMENT && $reader->moveToFirstAttribute()) {
        do { $reader->value; } while ($reader->moveToNextAttribute());
    }
}
