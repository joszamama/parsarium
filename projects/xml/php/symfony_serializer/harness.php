<?php
declare(strict_types=1);
require __DIR__ . '/autoload.php';
require __DIR__ . '/summary.php';

use Symfony\Component\Serializer\Encoder\XmlEncoder;

function parsarium_decode(string $bytes): mixed {
    return (new XmlEncoder())->decode($bytes, XmlEncoder::FORMAT);
}

function parsarium_parse(string $bytes): array {
    return parsarium_xml_encoder_summary(parsarium_decode($bytes));
}

if (PHP_SAPI === 'cli' && realpath($argv[0]) === __FILE__) {
    $bytes = file_get_contents($argv[1] ?? throw new InvalidArgumentException('input path required'));
    if ($bytes === false) { throw new RuntimeException('cannot read XML'); }
    echo json_encode(parsarium_parse($bytes), JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), "\n";
}
