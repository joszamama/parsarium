<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';
require __DIR__ . '/summary.php';

// XML_Parser 1.3.8 calls xml_set_object(), string handler names and xml_parser_free(), which PHP 8.4/8.5 deprecate
// but still run; run-control.php records those notices. Every other diagnostic stays visible.
error_reporting(E_ALL & ~E_DEPRECATED);

function parsarium_parse(string $bytes): array {
    return parsarium_xml_parser_summary('string', $bytes);
}

if (PHP_SAPI === 'cli' && realpath($argv[0]) === __FILE__) {
    $bytes = file_get_contents($argv[1] ?? throw new InvalidArgumentException('input path required'));
    if ($bytes === false) { throw new RuntimeException('cannot read XML'); }
    echo json_encode(parsarium_parse($bytes), JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), "\n";
}
