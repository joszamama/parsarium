<?php
declare(strict_types=1);
require __DIR__ . '/summary.php';

$path = $argv[1] ?? throw new InvalidArgumentException('input path required');
$bytes = file_get_contents($path);
if ($bytes === false) { throw new RuntimeException('cannot read XML'); }
libxml_use_internal_errors(true);
// The bytes are passed as a string; simplexml_load_file() (file/URL input) is not exercised.
$root = simplexml_load_string($bytes, SimpleXMLElement::class, LIBXML_NONET);
if ($root === false || libxml_get_errors() !== []) {
    throw new RuntimeException('XML parse error: ' . trim(libxml_get_errors()[0]->message ?? 'simplexml_load_string returned false'));
}
$summary = parsarium_xml_summary($root);
echo json_encode($summary, JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), "\n";
