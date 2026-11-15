<?php
declare(strict_types=1);

if ($argc !== 3 || !function_exists('xdebug_start_code_coverage')) {
    exit(2);
}
$input = file_get_contents($argv[1]);
if ($input === false) {
    exit(2);
}
require '/work/harness.php';
$function = getenv('PARSARIUM_PARSE_FUNCTION');
$prefix = getenv('PARSARIUM_SUBJECT_PREFIX');
if (!$function || !function_exists($function) || !$prefix) {
    exit(2);
}
xdebug_start_code_coverage();
try {
    $function($input);
} catch (Exception $rejected) {
    // Invalid inputs can raise ordinary parser exceptions. Their executed
    // parser lines still supply useful feedback; PHP Errors remain fatal.
}
$coverage = xdebug_get_code_coverage();
$features = [];
foreach ($coverage as $filename => $lines) {
    if (!str_starts_with($filename, $prefix)) {
        continue;
    }
    foreach ($lines as $line => $hits) {
        if ($hits > 0) {
            $features[] = $filename . ':' . $line;
        }
    }
}
sort($features);
if (file_put_contents($argv[2], implode("\n", $features) . "\n") === false) {
    exit(2);
}
