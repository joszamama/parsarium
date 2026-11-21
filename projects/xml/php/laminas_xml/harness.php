<?php
declare(strict_types=1);
require __DIR__ . '/autoload.php';
require __DIR__ . '/summary.php';

// Documented package entry point; returns the DOM document the package built from the bytes.
function parsarium_decode(string $bytes): DOMDocument {
    libxml_use_internal_errors(true);
    // Security::scan with a caller DOMDocument returns that DOMDocument after its heuristic DOCTYPE/entity checks.
    $document = Laminas\Xml\Security::scan($bytes, new DOMDocument());
    if (!$document instanceof DOMDocument) { throw new RuntimeException('Security::scan rejected the document'); }
    return $document;
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
