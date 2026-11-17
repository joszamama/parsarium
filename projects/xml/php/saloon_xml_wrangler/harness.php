<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';
require __DIR__ . '/summary.php';

use Saloon\XmlWrangler\XmlReader;

function parsarium_parse(string $bytes): array {
    return parsarium_wrangler_summary(XmlReader::fromString($bytes)->elements());
}

if (PHP_SAPI === 'cli' && realpath($argv[0]) === __FILE__) {
    $bytes = file_get_contents($argv[1] ?? throw new InvalidArgumentException('input path required'));
    if ($bytes === false) { throw new RuntimeException('cannot read XML'); }
    echo json_encode(parsarium_parse($bytes), JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), "\n";
}
