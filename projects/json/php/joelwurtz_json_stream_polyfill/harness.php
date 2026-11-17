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
            $members = new stdClass();
            foreach ($entries as [$name, $member]) { $members->{(string) $name} = $member; }
            return ['type' => 'object', 'members' => $members];
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
