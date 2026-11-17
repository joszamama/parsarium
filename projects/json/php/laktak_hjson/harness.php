<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';

use HJSON\HJSONParser;

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

function parsarium_parse(string $input): array {
    if ($input === '' || strlen($input) > (1 << 20)) {
        throw new InvalidArgumentException('input outside harness limit');
    }
    // HJSONParser splits the text into UTF-8 characters with preg_split('//u').
    if (!mb_check_encoding($input, 'UTF-8')) {
        throw new InvalidArgumentException('harness requires UTF-8 text');
    }
    return parsarium_tag((new HJSONParser())->parse($input));
}
