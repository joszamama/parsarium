<?php
declare(strict_types=1);
// PHP 8.5 reports deprecations in this package's source (some at compile time); they are kept off the
// output stream and do not change the parse. The base receipt records them separately.
error_reporting(E_ALL & ~E_DEPRECATED);
require __DIR__ . '/autoload.php';
require __DIR__ . '/summary.php';

// Documented package entry point; returns the DOM document the package built from the bytes.
function parsarium_decode(string $bytes): DOMDocument {
    libxml_use_internal_errors(true);
    $document = new DiDom\Document($bytes, false, 'UTF-8', DiDom\Document::TYPE_XML);
    // Document::getDocument() returns the DOMDocument that Document::load filled with DOMDocument::loadXML.
    return $document->getDocument();
}

function parsarium_parse(string $bytes): array {
    $document = parsarium_decode($bytes);
    if (libxml_get_errors() !== []) {
        throw new RuntimeException('XML parse error: ' . trim(libxml_get_errors()[0]->message));
    }
    return parsarium_xml_summary($document);
}

if (PHP_SAPI === 'cli' && realpath($argv[0]) === __FILE__) {
    $bytes = file_get_contents($argv[1] ?? throw new InvalidArgumentException('input path required'));
    if ($bytes === false) { throw new RuntimeException('cannot read XML'); }
    echo json_encode(parsarium_parse($bytes), JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), "\n";
}
