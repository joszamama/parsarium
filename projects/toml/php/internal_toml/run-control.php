<?php
declare(strict_types=1);
if (!function_exists('xdebug_start_code_coverage')) {
    throw new RuntimeException('Xdebug coverage extension is missing');
}
xdebug_start_code_coverage();
require __DIR__ . '/harness.php';
$data = file_get_contents('/input/control');
if ($data === false) { throw new RuntimeException('cannot read valid control'); }
$observed = parsarium_parse($data);
$raw = xdebug_get_code_coverage();
xdebug_stop_code_coverage();

$flags = JSON_PRETTY_PRINT | JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE;
$expectations = json_decode(file_get_contents(__DIR__ . '/target.json'), true, 512, JSON_THROW_ON_ERROR)
    ['expected_output_by_control_sha256'];
$digest = hash('sha256', $data);
if (!array_key_exists($digest, $expectations)) { throw new RuntimeException('unknown valid control'); }
// Typed-tree comparison: table keys are sorted on both sides (TOML key order is not significant).
$expected = json_encode(parsarium_canonical($expectations[$digest]), $flags);
if (json_encode($observed, $flags) !== $expected) {
    throw new RuntimeException('control mismatch: ' . json_encode($observed, $flags));
}
// The documented array API must agree with the AST walk's values (outside coverage).
if (serialize(Internal\Toml\Toml::parseToArray($data)) !== serialize(Internal\Toml\Toml::parse($data)->toArray())) {
    throw new RuntimeException('Toml::parseToArray() differs from Toml::parse()->toArray()');
}

$prefix = '/work/vendor/internal/toml/';
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
            'array_api_match' => true,
            'parser_source_files' => count($files), 'parser_source_lines_covered' => $total,
            'coverage' => '/coverage/coverage.json'];
file_put_contents('/coverage/observed.json', json_encode($observed, $flags) . "\n");
file_put_contents('/coverage/coverage.json', json_encode($coverage, $flags) . "\n");
file_put_contents('/coverage/summary.json', json_encode($summary, $flags) . "\n");
echo json_encode($summary, JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE), "\n";
