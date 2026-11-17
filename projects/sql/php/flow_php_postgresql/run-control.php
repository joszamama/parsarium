<?php
declare(strict_types=1);
// The documented sql_parse() call and the Traverser summary walk under Xdebug line coverage, writing the observed
// summary and the executed lines of the package and of its google/protobuf runtime.
const PACKAGE_PREFIX = '/work/vendor/flow-php/postgresql/';
const SUPPORT_PREFIX = '/work/vendor/google/protobuf/';
require __DIR__ . '/summary.php';

if (!function_exists('xdebug_start_code_coverage')) {
    throw new RuntimeException('Xdebug coverage extension is missing');
}
$data = file_get_contents('/input/control');
if ($data === false) { throw new RuntimeException('cannot read valid control'); }

xdebug_start_code_coverage();
$observed = parsarium_parse($data);
$raw = xdebug_get_code_coverage();
xdebug_stop_code_coverage();

// Xdebug reports one pseudo-line past the end of a class file on its first load; it is not source and is removed.
function parsarium_files(array $raw, string $prefix, int &$removed): array {
    $files = [];
    foreach ($raw as $filename => $lines) {
        if (!str_starts_with($filename, $prefix)) { continue; }
        $length = count(file($filename));
        $executed = [];
        foreach ($lines as $line => $hits) {
            if ($hits <= 0) { continue; }
            if ($line > $length) { $removed++; continue; }
            $executed[] = (int) $line;
        }
        sort($executed);
        $files[] = ['filename' => $filename,
                    'summary' => ['lines' => ['covered' => count($executed)]],
                    'executed_lines' => $executed];
    }
    usort($files, fn (array $a, array $b): int => strcmp($a['filename'], $b['filename']));
    return array_values(array_filter($files, fn (array $file): bool => $file['summary']['lines']['covered'] > 0));
}
$removed = 0;
$package = parsarium_files($raw, PACKAGE_PREFIX, $removed);
$support = parsarium_files($raw, SUPPORT_PREFIX, $removed);
$flags = JSON_PRETTY_PRINT | JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES;
file_put_contents('/coverage/observed.json', json_encode($observed, $flags) . "\n");
file_put_contents('/coverage/xdebug.json', json_encode([
    'package' => $package, 'support' => $support, 'xdebug_eof_pseudo_lines_removed' => $removed], $flags) . "\n");
