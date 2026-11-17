<?php
declare(strict_types=1);
if (!function_exists('xdebug_start_code_coverage')) {
    throw new RuntimeException('Xdebug coverage extension is missing');
}
const PACKAGE_PREFIX = '/work/vendor/saloonphp/xml-wrangler/';
const UNDERLYING_PREFIX = '/work/vendor/veewee/xml/';
require __DIR__ . '/vendor/autoload.php';
require __DIR__ . '/summary.php';

use Saloon\XmlWrangler\XmlReader;

$data = file_get_contents('/input/control');
if ($data === false) { throw new RuntimeException('cannot read valid control'); }
$target = json_decode(file_get_contents(__DIR__ . '/target.json'), true, 512, JSON_THROW_ON_ERROR);
$expected = $target['expected_output_by_control_sha256'][hash('sha256', $data)]
    ?? throw new RuntimeException('control is not one of the pinned valid controls');

// Coverage covers only the documented string entry point and elements().
xdebug_start_code_coverage();
$observed = parsarium_wrangler_summary(XmlReader::fromString($data)->elements());
$raw = xdebug_get_code_coverage();
xdebug_stop_code_coverage();
if ($observed !== $expected) { throw new RuntimeException('control mismatch: ' . json_encode($observed)); }
$fromFile = parsarium_wrangler_summary(XmlReader::fromFile('/input/control')->elements());
$stream = fopen('/input/control', 'rb');
$fromStream = parsarium_wrangler_summary(XmlReader::fromStream($stream)->elements());
if ($fromFile !== $observed || $fromStream !== $observed) {
    throw new RuntimeException('fromFile/fromStream summary differs from fromString');
}

function parsarium_files(array $raw, string $prefix): array {
    $files = [];
    foreach ($raw as $filename => $lines) {
        if (!str_starts_with($filename, $prefix)) { continue; }
        $executed = [];
        foreach ($lines as $line => $hits) { if ($hits > 0) { $executed[] = (int) $line; } }
        sort($executed);
        $files[] = ['filename' => $filename,
                    'summary' => ['lines' => ['covered' => count($executed)]],
                    'executed_lines' => $executed];
    }
    usort($files, fn (array $a, array $b): int => strcmp($a['filename'], $b['filename']));
    return $files;
}
$package = parsarium_files($raw, PACKAGE_PREFIX);
$underlying = parsarium_files($raw, UNDERLYING_PREFIX);
$count = fn (array $files): int => array_sum(array_map(fn (array $f): int => $f['summary']['lines']['covered'], $files));
if ($count($package) === 0 || $count($underlying) === 0) {
    throw new RuntimeException('no XML Wrangler or veewee/xml source lines covered');
}
$coverage = ['data' => [['files' => [...$package, ...$underlying]]]];
$summary = ['control_pass' => true, 'output' => $observed, 'file_and_stream_api_match' => true,
            'parser_source_files' => count($package), 'parser_source_lines_covered' => $count($package),
            'underlying_source_files' => count($underlying),
            'underlying_source_lines_covered' => $count($underlying),
            'coverage' => '/coverage/coverage.json'];
$flags = JSON_PRETTY_PRINT | JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE;
file_put_contents('/coverage/observed.json', json_encode($observed, $flags) . "\n");
file_put_contents('/coverage/coverage.json', json_encode($coverage, $flags) . "\n");
file_put_contents('/coverage/summary.json', json_encode($summary, $flags) . "\n");
echo json_encode($summary, JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE), "\n";
