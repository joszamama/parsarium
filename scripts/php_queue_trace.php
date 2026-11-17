<?php
declare(strict_types=1);

// Mounted read-only into the verified PHP control image. This invokes the
// project's existing byte-input parser once; it never starts a fuzz campaign.
[$script, $case, $output, $prefixesJson] = $argv;
$prefixes = json_decode($prefixesJson, true, 512, JSON_THROW_ON_ERROR);
if (!is_array($prefixes) || $prefixes === []) {
    throw new RuntimeException('expected parser source prefixes');
}
foreach ($prefixes as $prefix) {
    if (!is_string($prefix) || !str_starts_with($prefix, '/')) {
        throw new RuntimeException('expected absolute parser source prefixes');
    }
}
if (!function_exists('xdebug_start_code_coverage')) {
    throw new RuntimeException('verified PHP image lacks Xdebug line coverage');
}
xdebug_start_code_coverage();
require '/work/harness.php';
if (!function_exists('parsarium_parse')) {
    throw new RuntimeException('project has no parsarium_parse byte-input harness');
}
$bytes = file_get_contents($case);
if ($bytes === false) {
    throw new RuntimeException('cannot read saved input');
}
$outcome = 'ok';
try {
    parsarium_parse($bytes);
} catch (Throwable $error) {
    $outcome = 'exception:' . get_class($error);
}
$files = [];
foreach (xdebug_get_code_coverage() as $filename => $lines) {
    $selected = false;
    foreach ($prefixes as $prefix) {
        if (str_starts_with($filename, $prefix)) {
            $selected = true;
            break;
        }
    }
    if (!$selected) {
        continue;
    }
    $executed = [];
    foreach ($lines as $line => $hits) {
        if ($hits > 0) {
            $executed[] = (int) $line;
        }
    }
    sort($executed, SORT_NUMERIC);
    if ($executed !== []) {
        $files[] = ['filename' => $filename, 'executed_lines' => $executed];
    }
}
usort($files, fn ($a, $b) => strcmp($a['filename'], $b['filename']));
$record = ['outcome' => $outcome, 'files' => $files];
$json = json_encode($record, JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE);
file_put_contents($output, $json . "\n");
