<?php
declare(strict_types=1);
// Counts calls made from package source lines (call-site line > callee) for one
// input, using an Xdebug function trace. Run with xdebug.mode=trace and
// xdebug.use_compression=0; argv: input path, harness function.
require __DIR__ . '/harness.php';

const PACKAGE = '/work/vendor/cerbero/json-parser/';

$function = $argv[2];
if (!in_array($function, ['parsarium_parse', 'parsarium_no_parse'], true)) { exit(2); }
$input = file_get_contents($argv[1]);
if ($input === false) { exit(2); }
$trace = xdebug_start_trace('/tmp/parsarium-calls', XDEBUG_TRACE_COMPUTERIZED);
$function($input);
xdebug_stop_trace();
$counts = [];
foreach (file($trace, FILE_IGNORE_NEW_LINES) as $row) {
    // Computerized entry rows: level, id, 0, time, memory, function, user, include, file, line, ...
    $field = explode("\t", $row);
    if (count($field) < 10 || $field[2] !== '0' || !str_starts_with($field[8], PACKAGE)) { continue; }
    $site = substr($field[8], strlen(PACKAGE)) . ':' . $field[9] . '>' . $field[5];
    $counts[$site] = ($counts[$site] ?? 0) + 1;
}
ksort($counts, SORT_STRING);
echo json_encode((object) $counts, JSON_THROW_ON_ERROR), "\n";
