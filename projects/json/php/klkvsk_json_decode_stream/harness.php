<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';
// v1.0.3 (2021) implements Iterator/IteratorAggregate without return types, which PHP 8.1+
// reports as E_DEPRECATED when the classes load; php-fuzzer would turn that notice into a
// crash. The classes still run unchanged. Every other diagnostic stays visible.
error_reporting(E_ALL & ~E_DEPRECATED);

use JsonDecodeStream\Parser;

// Type-tags a decoded PHP value: stdClass -> object (members in returned order),
// list array -> array, scalars by PHP type. Anything else is rejected.
function parsarium_tag(mixed $value): array {
    if ($value === null) { return ['type' => 'null']; }
    if (is_bool($value)) { return ['type' => 'boolean', 'value' => $value]; }
    if (is_int($value) || is_float($value)) { return ['type' => 'number', 'value' => $value]; }
    if (is_string($value)) { return ['type' => 'string', 'value' => $value]; }
    if ($value instanceof stdClass) {
        $members = new stdClass();
        foreach (get_object_vars($value) as $name => $member) { $members->{(string) $name} = parsarium_tag($member); }
        return ['type' => 'object', 'members' => $members];
    }
    if (is_array($value) && array_is_list($value)) {
        return ['type' => 'array', 'items' => array_map('parsarium_tag', $value)];
    }
    throw new UnexpectedValueException('unexpected decoded value: ' . get_debug_type($value));
}

// items() with no selector yields each complete top-level document; objects are stdClass.
function parsarium_documents(Parser $parser): array {
    $documents = [];
    foreach ($parser->items() as $document) { $documents[] = $document; }
    if (count($documents) !== 1) {
        throw new UnexpectedValueException('harness requires exactly one complete document');
    }
    return parsarium_tag($documents[0]);
}

function parsarium_parse(string $input): array {
    if ($input === '' || strlen($input) > (1 << 20)) {
        throw new InvalidArgumentException('input outside harness limit');
    }
    return parsarium_documents(Parser::fromString($input));
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
