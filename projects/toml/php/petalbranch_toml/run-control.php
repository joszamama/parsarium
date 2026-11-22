<?php
declare(strict_types=1);
if (!function_exists('xdebug_start_code_coverage')) {
    throw new RuntimeException('Xdebug coverage extension is missing');
}
require __DIR__ . '/harness.php';
$data = file_get_contents('/input/control');
if ($data === false) { throw new RuntimeException('cannot read valid control'); }
// Coverage starts after the autoloader is loaded: Composer eagerly includes the package's
// src/functions.php (toml_decode/toml_encode helpers), which is not parsing. The AFL++ bridge
// (php_trace.php) also starts coverage after requiring the harness.
xdebug_start_code_coverage();
$observed = parsarium_parse($data);
$raw = xdebug_get_code_coverage();
xdebug_stop_code_coverage();

$flags = JSON_PRETTY_PRINT | JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE;
$expectations = json_decode(file_get_contents(__DIR__ . '/target.json'), true, 512, JSON_THROW_ON_ERROR)
    ['expected_output_by_control_sha256'];
$digest = hash('sha256', $data);
// Typed-tree comparison: table keys are sorted on both sides (TOML key order is not significant).
// Any other valid input reports the typed tree the parser produced in the mismatch message.
if (!array_key_exists($digest, $expectations)
        || json_encode($observed, $flags) !== json_encode(parsarium_canonical($expectations[$digest]), $flags)) {
    throw new RuntimeException('control mismatch: ' . json_encode($observed, $flags));
}
// The node tree's own getValue() must equal the documented array APIs Toml::parse() and
// Toml::parseFile() (outside coverage).
$normalized = serialize((new Petalbranch\Toml\Parser\Parser(new Petalbranch\Toml\Parser\Lexer()))
    ->parseToNode($data)->getValue());
if (serialize(Petalbranch\Toml\Toml::parse($data)) !== $normalized
        || serialize(Petalbranch\Toml\Toml::parseFile('/input/control')) !== $normalized) {
    throw new RuntimeException('Toml::parse() or Toml::parseFile() differs from the parseToNode() tree');
}

$prefix = '/work/vendor/petalbranch/toml/';
$files = [];
$total = 0;
foreach ($raw as $filename => $lines) {
    if (!str_starts_with($filename, $prefix)) { continue; }
    $executed = [];
    foreach ($lines as $line => $hits) { if ($hits > 0) { $executed[] = (int) $line; } }
    sort($executed);
    $total += count($executed);
    $files[] = ['filename' => $filename,
                'summary' => ['lines' => ['covered' => count($executed)]],
                'executed_lines' => $executed];
}
usort($files, fn (array $a, array $b): int => strcmp($a['filename'], $b['filename']));
if ($total === 0) { throw new RuntimeException('no PHP parser package source lines covered'); }
$coverage = ['data' => [['files' => $files]]];
$summary = ['control_pass' => true, 'control_sha256' => $digest, 'output' => $observed,
            'parse_and_parse_file_match' => true,
            'parser_source_files' => count($files), 'parser_source_lines_covered' => $total,
            'coverage' => '/coverage/coverage.json'];
file_put_contents('/coverage/observed.json', json_encode($observed, $flags) . "\n");
file_put_contents('/coverage/coverage.json', json_encode($coverage, $flags) . "\n");
file_put_contents('/coverage/summary.json', json_encode($summary, $flags) . "\n");
echo json_encode($summary, JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE), "\n";
