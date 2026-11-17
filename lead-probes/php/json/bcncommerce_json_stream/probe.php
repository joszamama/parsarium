<?php
declare(strict_types=1);
// Reads one valid control through the documented Reader::read() and reports the
// returned PHP value with PHP-level type tags plus the executed package lines.
require '/work/vendor/autoload.php';

const PACKAGE_PREFIX = '/work/vendor/bcncommerce/json-stream/';

function probe_tag(mixed $value): array {
    if ($value === null) { return ['type' => 'null']; }
    if (is_bool($value)) { return ['type' => 'boolean', 'value' => $value]; }
    if (is_int($value)) { return ['type' => 'integer', 'value' => $value]; }
    if (is_float($value)) { return ['type' => 'float', 'value' => $value]; }
    if (is_string($value)) { return ['type' => 'string', 'value' => $value]; }
    if ($value instanceof stdClass) {
        $vars = get_object_vars($value);
        return ['type' => 'object', 'members' => array_map(null, array_map('strval', array_keys($vars)),
            array_map('probe_tag', array_values($vars)))];
    }
    if (is_array($value) && $value !== [] && !array_is_list($value)) {
        return ['type' => 'php_assoc_array', 'members' => array_map(null, array_map('strval', array_keys($value)),
            array_map('probe_tag', array_values($value)))];
    }
    if (is_array($value)) { return ['type' => 'php_list', 'items' => array_map('probe_tag', $value)]; }
    throw new UnexpectedValueException(get_debug_type($value));
}

xdebug_start_code_coverage();
$handle = fopen('/input/control', 'rb');
$value = (new Bcn\Component\Json\Reader($handle))->read();
fclose($handle);
$coverage = xdebug_get_code_coverage();
xdebug_stop_code_coverage();
$lines = [];
foreach ($coverage as $file => $hits) {
    if (!str_starts_with($file, PACKAGE_PREFIX)) { continue; }
    foreach ($hits as $line => $count) {
        if ($count > 0) { $lines[] = substr($file, strlen(PACKAGE_PREFIX)) . ':' . $line; }
    }
}
sort($lines);
echo json_encode(['tree' => probe_tag($value), 'package_lines' => $lines],
    JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_PRESERVE_ZERO_FRACTION), "\n";
