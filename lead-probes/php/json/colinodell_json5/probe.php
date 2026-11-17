<?php
declare(strict_types=1);
// Decodes each valid control through both documented APIs and records which package lines ran.
if (!function_exists('xdebug_start_code_coverage')) {
    throw new RuntimeException('Xdebug coverage extension is missing');
}
require __DIR__ . '/vendor/autoload.php';

use ColinODell\Json5\Json5Decoder;

const PACKAGE = '/work/vendor/colinodell/json5/';

// Ordered type-tagged tree; integers and floats stay distinct.
function parsarium_tagged(mixed $value): array {
    return match (true) {
        $value === null => ['type' => 'null'],
        is_bool($value) => ['type' => 'boolean', 'value' => $value],
        is_int($value) => ['type' => 'integer', 'value' => (string) $value],
        is_float($value) => ['type' => 'float', 'value' => $value],
        is_string($value) => ['type' => 'string', 'value' => $value],
        is_array($value) && array_is_list($value) => ['type' => 'array', 'items' => array_map('parsarium_tagged', $value)],
        $value instanceof stdClass => ['type' => 'object', 'members' => array_map(
            static fn (string|int $key, mixed $child): array => [(string) $key, parsarium_tagged($child)],
            array_keys(get_object_vars($value)), array_values(get_object_vars($value)))],
        default => throw new UnexpectedValueException('unexpected decoded value: ' . get_debug_type($value)),
    };
}

$apis = [
    'Json5Decoder::decode' => static fn (string $text): mixed => Json5Decoder::decode($text),
    'json5_decode' => static fn (string $text): mixed => json5_decode($text),
];
$runs = [];
foreach (array_slice($argv, 1) as $path) {
    $text = file_get_contents($path);
    if ($text === false) { throw new RuntimeException("cannot read $path"); }
    foreach ($apis as $api => $call) {
        xdebug_start_code_coverage();
        $value = $call($text);
        $raw = xdebug_get_code_coverage();
        xdebug_stop_code_coverage();
        $lines = [];
        foreach ($raw as $file => $hits) {
            if (!str_starts_with($file, PACKAGE)) { continue; }
            $executed = array_keys(array_filter($hits, static fn (int $hit): bool => $hit > 0));
            sort($executed);
            if ($executed !== []) { $lines[substr($file, strlen(PACKAGE))] = $executed; }
        }
        $runs[] = ['control' => basename($path), 'api' => $api, 'tree' => parsarium_tagged($value),
                   'identical_to_json_decode' => $value == json_decode($text, false, 512, JSON_THROW_ON_ERROR),
                   'package_lines_executed' => $lines];
    }
}
echo json_encode(['php' => PHP_VERSION, 'xdebug' => phpversion('xdebug'),
                  'toolchain' => file(__DIR__ . '/toolchain.txt', FILE_IGNORE_NEW_LINES),
                  'runs' => $runs], JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_PRESERVE_ZERO_FRACTION), "\n";
