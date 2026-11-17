#!/opt/php/bin/php
<?php
declare(strict_types=1);
require __DIR__ . '/summary.php';

// Parse-time target: the documented pg_query_parse() on one local input. The JSON decode and summary walk of
// harness.php are skipped (neither runs instrumented C code). Executable through its #! line so that afl-showmap
// can start it as a single program with the input path as the only argument.
$path = $argv[1] ?? null;
if ($path === null || !is_file($path) || filesize($path) > (1 << 20)) { exit(0); }
$bytes = file_get_contents($path);
if ($bytes === false || $bytes === '') { exit(0); }
try {
    parsarium_pg_query_parse($bytes);
} catch (RuntimeException) {
    // pg_query_parse() reports rejected SQL as a RuntimeException.
}
