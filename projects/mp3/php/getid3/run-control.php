<?php
declare(strict_types=1);

if (!function_exists('xdebug_start_code_coverage')) {
    throw new RuntimeException('Xdebug coverage extension is missing');
}
xdebug_start_code_coverage();
require __DIR__ . '/harness.php';
$data = file_get_contents('/input/control');
if ($data === false) {
    throw new RuntimeException('Could not read valid control');
}
$observed = parsarium_parse_mp3($data);
$expected = ['mpeg_version' => '1', 'layer' => 3, 'sample_rate' => 44100, 'channels' => 1,
             'channelmode' => 'mono', 'bitrate' => 64000, 'bitrate_mode' => 'cbr', 'framelength' => 208,
             'playtime_seconds' => 0.28725, 'audio_data_bytes' => 2298, 'tag_formats' => []];
if ($observed !== $expected) {
    throw new RuntimeException('Control mismatch: ' . json_encode($observed));
}
$raw = xdebug_get_code_coverage();
$files = [];
$total = 0;
foreach ($raw as $filename => $lines) {
    if (!str_starts_with($filename, '/work/vendor/james-heinrich/getid3/')) {
        continue;
    }
    $executed = [];
    foreach ($lines as $line => $hits) {
        if ($hits > 0) {
            $executed[] = (int) $line;
        }
    }
    sort($executed);
    $total += count($executed);
    $files[] = ['filename' => $filename,
                'summary' => ['lines' => ['covered' => count($executed)]],
                'executed_lines' => $executed];
}
if ($total === 0) {
    throw new RuntimeException('No PHP package source lines covered');
}
$coverage = ['data' => [['files' => $files]]];
$summary = ['control_pass' => true, 'output' => $observed,
            'parser_source_files' => count($files),
            'parser_source_lines_covered' => $total,
            'coverage' => '/coverage/coverage.json'];
file_put_contents('/coverage/observed.json', json_encode($observed, JSON_PRETTY_PRINT | JSON_THROW_ON_ERROR) . "\n");
file_put_contents('/coverage/coverage.json', json_encode($coverage, JSON_PRETTY_PRINT | JSON_THROW_ON_ERROR) . "\n");
file_put_contents('/coverage/summary.json', json_encode($summary, JSON_PRETTY_PRINT | JSON_THROW_ON_ERROR) . "\n");
echo json_encode($summary, JSON_THROW_ON_ERROR), "\n";
