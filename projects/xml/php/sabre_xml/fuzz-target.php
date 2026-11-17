<?php
declare(strict_types=1);
require __DIR__ . '/autoload.php';

$path = $argv[1] ?? null;
if ($path === null || !is_file($path) || filesize($path) > (1 << 20)) { exit(0); }
$bytes = file_get_contents($path);
if ($bytes === false || $bytes === '') { exit(0); }
try {
    $reader = (new Sabre\Xml\Service())->getReader();
    $reader->XML($bytes, null, LIBXML_NONET);
    $reader->parse();
} catch (Sabre\Xml\ParseException) {
}
