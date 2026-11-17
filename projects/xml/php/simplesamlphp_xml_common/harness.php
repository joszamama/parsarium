<?php
declare(strict_types=1);
require __DIR__ . '/autoload.php';
require __DIR__ . '/summary.php';

use SimpleSAML\XML\DOMDocumentFactory;

// Documented package entry point with its default options (LIBXML_COMPACT | LIBXML_NONET | LIBXML_NSCLEAN |
// LIBXML_NO_XXE); it rejects whitespace-only input and DOCTYPE markup and returns a Dom\XMLDocument.
function parsarium_decode(string $bytes): Dom\XMLDocument {
    return DOMDocumentFactory::fromString($bytes);
}

function parsarium_parse(string $bytes): array {
    return parsarium_xml_summary(parsarium_decode($bytes));
}

if (PHP_SAPI === 'cli' && realpath($argv[0]) === __FILE__) {
    $bytes = file_get_contents($argv[1] ?? throw new InvalidArgumentException('input path required'));
    if ($bytes === false) { throw new RuntimeException('cannot read XML'); }
    echo json_encode(parsarium_parse($bytes), JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), "\n";
}
