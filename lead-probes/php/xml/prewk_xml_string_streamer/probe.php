<?php
declare(strict_types=1);
// Streams each valid control through the documented file, handle and UniqueNode APIs and records
// the returned node strings, which package lines ran, and which PHP XML parser APIs the source calls.
if (!function_exists('xdebug_start_code_coverage')) {
    throw new RuntimeException('Xdebug coverage extension is missing');
}
require __DIR__ . '/vendor/autoload.php';

use Prewk\XmlStringStreamer;
use Prewk\XmlStringStreamer\Parser;
use Prewk\XmlStringStreamer\Stream;

const PACKAGE = '/work/vendor/prewk/xml-string-streamer/';
// A small chunk size makes the handle route cross several chunk boundaries on both controls.
const HANDLE_CHUNK_BYTES = 7;

$apis = [
    'createStringWalkerParser(path)' => static fn (string $path, string $unique): XmlStringStreamer =>
        XmlStringStreamer::createStringWalkerParser($path),
    'StringWalker+Stream\File(handle)' => static fn (string $path, string $unique): XmlStringStreamer =>
        new XmlStringStreamer(new Parser\StringWalker(), new Stream\File(fopen($path, 'rb'), HANDLE_CHUNK_BYTES)),
    'createUniqueNodeParser(path)' => static fn (string $path, string $unique): XmlStringStreamer =>
        XmlStringStreamer::createUniqueNodeParser($path, ['uniqueNode' => $unique]),
];
$runs = [];
foreach (array_slice($argv, 1) as $argument) {
    [$path, $unique] = explode('=', $argument, 2);
    foreach ($apis as $api => $create) {
        xdebug_start_code_coverage();
        $streamer = $create($path, $unique);
        $nodes = [];
        while (($node = $streamer->getNode()) !== false) {
            $nodes[] = $node;
        }
        unset($streamer);
        $raw = xdebug_get_code_coverage();
        xdebug_stop_code_coverage();
        $lines = [];
        foreach ($raw as $file => $hits) {
            if (!str_starts_with($file, PACKAGE)) { continue; }
            $executed = array_keys(array_filter($hits, static fn (int $hit): bool => $hit > 0));
            sort($executed);
            if ($executed !== []) { $lines[substr($file, strlen(PACKAGE))] = $executed; }
        }
        ksort($lines);
        $runs[] = ['control' => basename($path), 'api' => $api,
                   'unique_node' => str_starts_with($api, 'createUniqueNode') ? $unique : null,
                   'nodes_base64' => array_map('base64_encode', $nodes),
                   'package_lines_executed' => $lines];
    }
}
$calls = [];
$sources = new RecursiveIteratorIterator(new RecursiveDirectoryIterator(PACKAGE . 'src', FilesystemIterator::SKIP_DOTS));
foreach ($sources as $file) {
    $text = file_get_contents($file->getPathname());
    foreach (['simplexml_', 'XMLReader', 'XMLParser', 'xml_parser_create', 'DOMDocument', 'libxml_', 'preg_match'] as $name) {
        if (stripos($text, $name) !== false) { $calls[$name][] = substr($file->getPathname(), strlen(PACKAGE)); }
    }
}
ksort($calls);
echo json_encode(['php' => PHP_VERSION, 'xdebug' => phpversion('xdebug'),
                  'toolchain' => file(__DIR__ . '/toolchain.txt', FILE_IGNORE_NEW_LINES),
                  'source_api_mentions' => $calls, 'runs' => $runs],
                 JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), "\n";
