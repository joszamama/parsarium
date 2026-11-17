<?php
declare(strict_types=1);
// Reads one valid control as a local stream through the documented
// JsonStreamReader::read(resource, Type) with the schema-free Type::mixed(), and
// reports the returned PHP value with PHP-level type tags plus executed package lines.
require '/work/vendor/autoload.php';

use Symfony\Component\JsonStreamer\JsonStreamReader;
use Symfony\Component\TypeInfo\Type;

const PACKAGE_PREFIX = '/work/vendor/symfony/json-streamer/';

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
$reader = JsonStreamReader::create(streamReadersDir: '/tmp/stream-readers');
$handle = fopen('/input/control', 'rb');
$value = $reader->read($handle, Type::mixed());
fclose($handle);
$coverage = xdebug_get_code_coverage();
xdebug_stop_code_coverage();
$lines = [];
foreach ($coverage as $file => $hits) {
    if (str_starts_with($file, '/tmp/stream-readers/')) { $lines[] = 'generated:' . basename($file) . ':' . count(array_filter($hits, fn ($c) => $c > 0)); continue; }
    if (!str_starts_with($file, PACKAGE_PREFIX)) { continue; }
    foreach ($hits as $line => $count) {
        if ($count > 0) { $lines[] = substr($file, strlen(PACKAGE_PREFIX)) . ':' . $line; }
    }
}
sort($lines);
$generated = glob('/tmp/stream-readers/*.php');
echo json_encode(['tree' => probe_tag($value), 'package_lines' => $lines,
                  'generated_reader' => $generated ? file_get_contents($generated[0]) : null],
    JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_PRESERVE_ZERO_FRACTION), "\n";
