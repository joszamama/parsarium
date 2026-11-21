<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';
// The image removes the package's Composer "files" autoload entry so that php-fuzzer
// instruments the polyfill; load it with the README's documented manual require.
require __DIR__ . '/vendor/joelwurtz/json-stream-polyfill/bootstrap.php';

use JsonStream\Document;

if (extension_loaded('json_stream')) {
    throw new RuntimeException('json_stream extension loaded; the pure-PHP polyfill would be inert');
}

// Walks a lazy JsonStream\Document with foreach (slot mode): the package scans
// container structure itself and yields child Documents for nested containers.
// The container kind comes from the documented __debugInfo() 'kind'. Scalars
// are the values the package yields; toValue() is never called.
function parsarium_tag(mixed $value): array {
    if ($value instanceof Document) {
        $entries = [];
        try {
            foreach ($value as $name => $member) { $entries[] = [$name, parsarium_tag($member)]; }
        } catch (\Error $error) {
            if ($value->__debugInfo()['kind'] !== 'scalar') { throw $error; }
            return parsarium_tag($value->__debugInfo()['value']);
        }
        $kind = $value->__debugInfo()['kind'];
        if ($kind === 'object') {
            $members = [];
            foreach ($entries as [$name, $member]) { $members[(string) $name] = $member; }
            return ['type' => 'object', 'members' => parsarium_members($members)];
        }
        if ($kind === 'array') {
            return ['type' => 'array', 'items' => array_column($entries, 1)];
        }
        throw new UnexpectedValueException('unexpected document kind: ' . $kind);
    }
    if ($value === null) { return ['type' => 'null']; }
    if (is_bool($value)) { return ['type' => 'boolean', 'value' => $value]; }
    if (is_int($value) || is_float($value)) { return ['type' => 'number', 'value' => $value]; }
    if (is_string($value)) { return ['type' => 'string', 'value' => $value]; }
    throw new UnexpectedValueException('unexpected decoded value: ' . get_debug_type($value));
}

function parsarium_parse(string $input): array {
    if ($input === '' || strlen($input) > (1 << 20)) {
        throw new InvalidArgumentException('input outside harness limit');
    }
    // Documented json_stream_decode(string) with default options (slot mode, not
    // JSON_STREAM_TRANSIENT). Full iteration reaches the root's closing bracket,
    // where the package rejects trailing bytes.
    return parsarium_tag(json_stream_decode($input));
}

// json_encode() cannot write INF or NAN. A float infinity the parser returned (for
// an out-of-range exponent) is written as an Infinity/-Infinity/NaN token, which
// Python's json module reads, so the value stays a number in the reported result.
function parsarium_json_text(mixed $value, int $flags): string {
    $marker = "\u{1}parsarium-nonfinite\u{1}";
    $map = function (mixed $item) use (&$map, $marker): mixed {
        if (is_float($item) && !is_finite($item)) {
            return $marker . (is_nan($item) ? 'NaN' : ($item > 0 ? 'Infinity' : '-Infinity'));
        }
        if (is_array($item)) { return array_map($map, $item); }
        if ($item instanceof stdClass) { return (object) array_map($map, get_object_vars($item)); }
        return $item;
    };
    $text = json_encode($map($value), $flags | JSON_THROW_ON_ERROR);
    foreach (['NaN', 'Infinity', '-Infinity'] as $token) {
        $text = str_replace(json_encode($marker . $token, $flags | JSON_THROW_ON_ERROR), $token, $text);
    }
    return $text;
}

// Object members collected in a PHP array. A stdClass cannot hold a property whose
// name starts with "\0" (a valid JSON key such as "\u0000"); such members stay an
// array, which json_encode() still writes as a JSON object.
function parsarium_members(array $members): array|stdClass {
    foreach (array_keys($members) as $name) {
        if (str_starts_with((string) $name, "\0")) { return $members; }
    }
    return (object) $members;
}
