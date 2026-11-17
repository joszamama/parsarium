<?php
declare(strict_types=1);
// Parses /input/control through the string source under Xdebug, then checks the
// file and stream sources and records what reaches the package's JsonDecoder.
if (!function_exists('xdebug_start_code_coverage')) {
    throw new RuntimeException('Xdebug coverage extension is missing');
}
xdebug_start_code_coverage();
require __DIR__ . '/harness.php';
$data = file_get_contents('/input/control');
if ($data === false) { throw new RuntimeException('cannot read valid control'); }
$tree = parsarium_parse($data);
$raw = xdebug_get_code_coverage();
xdebug_stop_code_coverage();

use Cerbero\JsonParser\Decoders\DecodedValue;
use Cerbero\JsonParser\Decoders\Decoder;
use Cerbero\JsonParser\Decoders\JsonDecoder;
use Cerbero\JsonParser\JsonParser;

const PACKAGE = '/work/vendor/cerbero/json-parser/';

$kind = parsarium_root_kind($data);
$fromFile = parsarium_tree(JsonParser::parse('/input/control'), $kind);
$handle = fopen('/input/control', 'rb');
$fromStream = parsarium_tree(JsonParser::parse($handle), $kind);
fclose($handle);

// Records every string the package hands to its default JsonDecoder.
final class ParsariumRecordingDecoder implements Decoder {
    public array $inputs = [];
    private JsonDecoder $inner;
    public function __construct() { $this->inner = new JsonDecoder(); }
    public function decode(string $json): DecodedValue {
        $this->inputs[] = $json;
        return $this->inner->decode($json);
    }
}
$compound = static fn (array $inputs): int => count(array_filter(
    $inputs, static fn (string $item): bool => $item[0] === '{' || $item[0] === '['));
$lazy = new ParsariumRecordingDecoder();
$lazyTree = parsarium_tree(JsonParser::parse($data)->decoder($lazy), $kind);
$eager = new ParsariumRecordingDecoder();
foreach (JsonParser::parse($data)->decoder($eager) as $unused) {}

$lines = [];
foreach ($raw as $file => $hits) {
    if (!str_starts_with($file, PACKAGE)) { continue; }
    $executed = array_keys(array_filter($hits, static fn (int $hit): bool => $hit > 0));
    sort($executed);
    if ($executed !== []) { $lines[substr($file, strlen(PACKAGE))] = $executed; }
}
ksort($lines, SORT_STRING);
echo json_encode([
    'php' => PHP_VERSION, 'xdebug' => phpversion('xdebug'),
    'toolchain' => file(__DIR__ . '/toolchain.txt', FILE_IGNORE_NEW_LINES),
    'control_sha256' => hash('sha256', $data),
    'tree' => $tree,
    'file_source_tree_identical' => $fromFile === $tree,
    'stream_source_tree_identical' => $fromStream === $tree,
    'decoder' => [
        'lazy_inputs' => count($lazy->inputs),
        'lazy_compound_inputs' => $compound($lazy->inputs),
        'lazy_tree_identical' => $lazyTree === $tree,
        'eager_inputs' => count($eager->inputs),
        'eager_compound_inputs' => $compound($eager->inputs),
        'eager_longest_input_bytes' => max(array_map('strlen', $eager->inputs)),
    ],
    'package_lines_executed' => $lines,
], JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_PRESERVE_ZERO_FRACTION), "\n";
