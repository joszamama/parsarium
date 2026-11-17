<?php
declare(strict_types=1);
require __DIR__ . '/autoload.php';
require __DIR__ . '/summary.php';

use Mtownsend\XmlToArray\XmlToArray;

// Documented entry point with the documented $outputRoot = true, so the root's tag name is returned as '@root'.
function parsarium_decode(string $bytes): array {
    return XmlToArray::convert($bytes, true);
}

function parsarium_parse(string $bytes): array {
    return parsarium_xml_to_array_summary(parsarium_decode($bytes));
}

if (PHP_SAPI === 'cli' && realpath($argv[0]) === __FILE__) {
    $bytes = file_get_contents($argv[1] ?? throw new InvalidArgumentException('input path required'));
    if ($bytes === false) { throw new RuntimeException('cannot read XML'); }
    // --raw prints convert()'s unmodified array, so namespace loss can be checked without the summary.
    $result = ($argv[2] ?? '') === '--raw' ? parsarium_decode($bytes) : parsarium_parse($bytes);
    echo json_encode($result, JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), "\n";
}
