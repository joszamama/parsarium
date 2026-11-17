<?php
declare(strict_types=1);
// jtrumbull/xml-parser v1.0.2 lead probe: run the documented XMLParser::decode(string) on each mounted valid
// control under Xdebug, and compare it with the same two PHP core calls made without the package
// (new SimpleXMLElement, then json_decode(json_encode(...))). Prints one JSON record.
require '/work/vendor/autoload.php';

const PACKAGE_PREFIX = '/work/vendor/jtrumbull/xml-parser/';
$results = [];
foreach (glob('/controls/*.xml') as $path) {
    $xml = file_get_contents($path);
    xdebug_start_code_coverage();
    $decoded = XMLParser\XMLParser::decode($xml);
    $coverage = xdebug_get_code_coverage();
    xdebug_stop_code_coverage();
    $bare = json_decode(json_encode(new SimpleXMLElement($xml)), false);
    $lines = [];
    foreach ($coverage as $file => $hits) {
        if (!str_starts_with($file, PACKAGE_PREFIX)) { continue; }
        $length = count(file($file));
        // Xdebug reports one pseudo-line past the end of a class file on first load; it is not source.
        $executed = array_values(array_filter(array_keys(array_filter($hits, fn ($hit) => $hit > 0)),
                                              fn ($line) => $line <= $length));
        sort($executed);
        $lines[substr($file, strlen(PACKAGE_PREFIX))] = $executed;
    }
    $results[basename($path)] = [
        'sha256' => hash('sha256', $xml),
        'decode' => $decoded,
        'identical_to_bare_simplexml_json' => json_encode($decoded) === json_encode($bare),
        'package_lines' => $lines,
    ];
}
echo json_encode(['php' => PHP_VERSION, 'libxml' => LIBXML_DOTTED_VERSION, 'results' => $results],
                 JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), "\n";
