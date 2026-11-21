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
$targets = json_decode(file_get_contents(__DIR__ . '/target.json'), true, 512, JSON_THROW_ON_ERROR)['expected_by_control_sha256'];
// Any other valid input reports what the package parsed in the mismatch message.
$expected = $targets[hash('sha256', $data)] ?? null;
if ($observed !== $expected) { throw new RuntimeException('control mismatch: ' . json_encode($observed)); }
$raw = xdebug_get_code_coverage();
$files = [];
$total = 0;
$encoder = 0;
foreach ($raw as $filename => $lines) {
    if (!str_starts_with($filename, '/work/vendor/symfony/serializer/')) { continue; }
    $executed = [];
    foreach ($lines as $line => $hits) { if ($hits > 0) { $executed[] = (int) $line; } }
    if ($executed === []) { continue; }
    sort($executed);
    $total += count($executed);
    if (str_ends_with($filename, '/Encoder/XmlEncoder.php')) { $encoder = count($executed); }
    $files[] = ['filename' => $filename,
                'summary' => ['lines' => ['covered' => count($executed)]],
                'executed_lines' => $executed];
}
if ($encoder === 0) { throw new RuntimeException('no XmlEncoder.php lines covered'); }
$coverage = ['data' => [['files' => $files]]];
$summary = ['control_pass' => true, 'output' => $observed,
            'parser_source_files' => count($files), 'parser_source_lines_covered' => $total,
            'format_specific_source_lines_covered' => $encoder,
            'coverage' => '/coverage/coverage.json'];
$flags = JSON_PRETTY_PRINT | JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE;
file_put_contents('/coverage/observed.json', json_encode($observed, $flags) . "\n");
file_put_contents('/coverage/coverage.json', json_encode($coverage, $flags) . "\n");
file_put_contents('/coverage/summary.json', json_encode($summary, $flags) . "\n");
echo json_encode($summary, JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE), "\n";
