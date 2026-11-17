<?php
declare(strict_types=1);
require __DIR__ . '/summary.php';

// Parse-time target: yaml_parse() with the same YAML_MAP_TAG callback as the harness; the PHP tree walk and the
// JSON output of harness.php are skipped (neither runs instrumented C code).
$path = $argv[1] ?? null;
if ($path === null || !is_file($path) || filesize($path) > (1 << 20)) { exit(0); }
$bytes = file_get_contents($path);
if ($bytes === false || $bytes === '') { exit(0); }
// ext/yaml reports rejected input as an E_WARNING and returns false.
set_error_handler(static fn (): bool => true);
try {
    parsarium_yaml_parse($bytes);
} catch (RuntimeException) {
}
