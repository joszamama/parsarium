<?php
declare(strict_types=1);
require __DIR__ . '/summary.php';

$path = $argv[1] ?? throw new InvalidArgumentException('input path required');
$bytes = file_get_contents($path);
if ($bytes === false) { throw new RuntimeException('cannot read XML'); }
libxml_use_internal_errors(true);
$document = new DOMDocument();
// The bytes are passed as a string; DOMDocument::load() (file/URL input) is not exercised.
$loaded = $document->loadXML($bytes, LIBXML_NONET);
// libxml2 warnings (LIBXML_ERR_WARNING, such as "Unsupported version '1.1'") do not stop the parse; only errors fail.
$errors = array_values(array_filter(libxml_get_errors(), fn (LibXMLError $error): bool => $error->level !== LIBXML_ERR_WARNING));
if (!$loaded || $errors !== []) {
    throw new RuntimeException('XML parse error: ' . trim($errors[0]->message ?? 'loadXML returned false'));
}
$summary = parsarium_xml_summary($document);
echo json_encode($summary, JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), "\n";
