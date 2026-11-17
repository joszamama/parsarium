<?php
declare(strict_types=1);
// Package-line trace for one input: runs the same parse-only call as fuzz-target.php (sql_parse) under Xdebug and
// writes the executed flow-php/postgresql source lines as file:line features. Xdebug's pseudo-line past the end of
// a first-loaded class file is not source and is dropped.
if ($argc !== 3 || !function_exists('xdebug_start_code_coverage')) { exit(2); }
$input = file_get_contents($argv[1]);
if ($input === false) { exit(2); }
require '/work/summary.php';
$prefix = '/work/vendor/flow-php/postgresql/';
xdebug_start_code_coverage();
try {
    parsarium_sql_parse($input);
} catch (Flow\PostgreSql\Exception\ParserException) {
}
$coverage = xdebug_get_code_coverage();
xdebug_stop_code_coverage();
$features = [];
foreach ($coverage as $filename => $lines) {
    if (!str_starts_with($filename, $prefix)) { continue; }
    $length = count(file($filename));
    foreach ($lines as $line => $hits) {
        if ($hits > 0 && $line <= $length) { $features[] = $filename . ':' . $line; }
    }
}
sort($features);
if (file_put_contents($argv[2], implode("\n", $features) . "\n") === false) { exit(2); }
