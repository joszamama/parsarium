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
$expected = json_decode("{\"width\": 2, \"height\": 1}", true, 512, JSON_THROW_ON_ERROR);
if ($observed != $expected) { throw new RuntimeException('control mismatch: ' . json_encode($observed)); }
$raw = xdebug_get_code_coverage();
$files = [];
$total = 0;
$primaryFiles = 0;
$underlyingFiles = 0;
$underlyingLines = 0;
foreach ($raw as $filename => $lines) {
    $primary = str_starts_with($filename, "/work/vendor/intervention/image-laravel/");
    $underlying = str_starts_with($filename, "/work/vendor/intervention/image/src/");
    if (!$primary && !$underlying) { continue; }
    $executed = [];
    foreach ($lines as $line => $hits) { if ($hits > 0) { $executed[] = (int) $line; } }
    sort($executed);
    if ($primary) {
        $primaryFiles++;
        $total += count($executed);
    }
    if ($underlying) {
        $underlyingFiles++;
        $underlyingLines += count($executed);
    }
    $files[] = ['filename' => $filename,
                'summary' => ['lines' => ['covered' => count($executed)]],
                'executed_lines' => $executed];
}
if ($total === 0) { throw new RuntimeException('no PHP parser package source lines covered'); }
if ($underlyingLines === 0) { throw new RuntimeException('no Intervention Image source covered'); }
$coverage = ['data' => [['files' => $files]]];
$summary = ['control_pass' => true, 'output' => $observed,
            'parser_source_files' => $primaryFiles, 'parser_source_lines_covered' => $total,
            'underlying_source_files' => $underlyingFiles,
            'underlying_source_lines_covered' => $underlyingLines,
            'coverage' => '/coverage/coverage.json'];
file_put_contents('/coverage/observed.json', json_encode($observed, JSON_PRETTY_PRINT | JSON_THROW_ON_ERROR) . "\n");
file_put_contents('/coverage/coverage.json', json_encode($coverage, JSON_PRETTY_PRINT | JSON_THROW_ON_ERROR) . "\n");
file_put_contents('/coverage/summary.json', json_encode($summary, JSON_PRETTY_PRINT | JSON_THROW_ON_ERROR) . "\n");
echo json_encode($summary, JSON_THROW_ON_ERROR), "\n";
