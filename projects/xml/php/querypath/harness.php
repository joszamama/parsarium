<?php
declare(strict_types=1);
// PHP 8.5 reports deprecations in this package's source (some at compile time); they are kept off the
// output stream and do not change the parse. The base receipt records them separately.
error_reporting(E_ALL & ~E_DEPRECATED);
require __DIR__ . '/autoload.php';
require __DIR__ . '/summary.php';

// Documented package entry point; returns the DOM document the package built from the bytes.
// qp() picks its parser from the first five bytes: without a leading '<?xml' declaration it calls
// DOMDocument::loadHTML. The documented use_parser => 'xml' option selects the XML parser for every
// input (DOMQuery::parseXMLString); inputs that start with '<?xml' take the same path as before.
function parsarium_decode(string $bytes): DOMDocument {
    libxml_use_internal_errors(true);
    $qp = qp($bytes, null, ['use_parser' => 'xml']);
    // DOMQuery::document() returns the DOMDocument that QueryPath built with DOMDocument::loadXML.
    return $qp->document();
}

function parsarium_parse(string $bytes): array {
    $document = parsarium_decode($bytes);
    // libxml2 warnings (LIBXML_ERR_WARNING, such as "Unsupported version '1.1'") do not stop the parse; only errors fail.
    $errors = array_values(array_filter(libxml_get_errors(), fn (LibXMLError $error): bool => $error->level !== LIBXML_ERR_WARNING));
    if ($errors !== []) {
        throw new RuntimeException('XML parse error: ' . trim($errors[0]->message));
    }
    return parsarium_xml_summary($document);
}

if (PHP_SAPI === 'cli' && realpath($argv[0]) === __FILE__) {
    $bytes = file_get_contents($argv[1] ?? throw new InvalidArgumentException('input path required'));
    if ($bytes === false) { throw new RuntimeException('cannot read XML'); }
    echo json_encode(parsarium_parse($bytes), JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), "\n";
}
