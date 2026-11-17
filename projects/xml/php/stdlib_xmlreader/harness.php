<?php
declare(strict_types=1);
require __DIR__ . '/summary.php';

$path = $argv[1] ?? throw new InvalidArgumentException('input path required');
$bytes = file_get_contents($path);
if ($bytes === false) { throw new RuntimeException('cannot read XML'); }
libxml_use_internal_errors(true);
$reader = XMLReader::XML($bytes, null, LIBXML_NONET);
$summary = parsarium_xml_summary($reader);
if (libxml_get_errors() !== []) { throw new RuntimeException('XML parse error: ' . trim(libxml_get_errors()[0]->message)); }
echo json_encode($summary, JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), "\n";
