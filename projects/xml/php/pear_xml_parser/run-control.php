<?php
declare(strict_types=1);
// Mode "coverage": the documented setInputString() + parse() call under Xdebug line coverage, writing the
// observed summary, the package lines and the PHP deprecation notices. Mode "crosscheck": setInputFile(path) and
// setInput(resource) on the same control, printed as JSON (run without Xdebug, after the coverage process).
const PACKAGE_PREFIX = '/work/vendor/pear/xml_parser/';
const SUPPORT_PREFIX = '/work/vendor/pear/pear-core-minimal/';
require __DIR__ . '/vendor/autoload.php';
require __DIR__ . '/summary.php';

$deprecations = [];
set_error_handler(function (int $level, string $message, string $file, int $line) use (&$deprecations): bool {
    if ($level !== E_DEPRECATED) { throw new ErrorException($message, 0, $level, $file, $line); }
    $deprecations[str_replace('/work/vendor/', '', $file) . ':' . $line . ' ' . $message] = true;
    return true;
});
$mode = $argv[1] ?? 'coverage';
if ($mode === 'crosscheck') {
    $stream = fopen('/input/control', 'rb');
    echo json_encode(['file' => parsarium_xml_parser_summary('file', '/input/control'),
                      'stream' => parsarium_xml_parser_summary('stream', $stream)],
                     JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), "\n";
    exit(0);
}
if (!function_exists('xdebug_start_code_coverage')) {
    throw new RuntimeException('Xdebug coverage extension is missing');
}
$data = file_get_contents('/input/control');
if ($data === false) { throw new RuntimeException('cannot read valid control'); }

// Coverage covers only the documented string entry point and parse().
xdebug_start_code_coverage();
$observed = parsarium_xml_parser_summary('string', $data);
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
    return $files;
}
$removed = 0;
$package = parsarium_files($raw, PACKAGE_PREFIX, $removed);
$support = parsarium_files($raw, SUPPORT_PREFIX, $removed);
$flags = JSON_PRETTY_PRINT | JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES;
file_put_contents('/coverage/observed.json', json_encode($observed, $flags) . "\n");
file_put_contents('/coverage/xdebug.json', json_encode([
    'package' => $package, 'support' => $support, 'xdebug_eof_pseudo_lines_removed' => $removed,
    'php_deprecations' => array_keys($deprecations)], $flags) . "\n");
