<?php
declare(strict_types=1);
require __DIR__ . '/summary.php';

$path = $argv[1] ?? throw new InvalidArgumentException('input path required');
$bytes = file_get_contents($path);
if ($bytes === false) { throw new RuntimeException('cannot read XML'); }
// The bytes go to xml_parse in one final chunk; the summary is collected by the event handlers during the parse.
$summary = parsarium_xml_parse($bytes);
echo json_encode($summary, JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), "\n";
