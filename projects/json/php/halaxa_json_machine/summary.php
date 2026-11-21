<?php
declare(strict_types=1);

// A JSON object a harness assembles itself from parser events, members in order.
// Unlike stdClass it can hold a member whose name starts with "\0" (e.g. "\u0000").
final class ParsariumObject {
    public array $members = [];
}

// Shared observable summary of a decoded JSON value (stdClass or ParsariumObject
// objects, lists, scalars).
function parsarium_json_summary(mixed $root): array {
    $counts = ['objects' => 0, 'arrays' => 0, 'booleans' => 0, 'nulls' => 0];
    $strings = [];
    $numbers = [];
    $maxDepth = 0;
    $walk = function (mixed $value, int $depth) use (&$walk, &$counts, &$strings, &$numbers, &$maxDepth): void {
        if ($value instanceof stdClass || $value instanceof ParsariumObject) {
            $counts['objects']++;
            $maxDepth = max($maxDepth, $depth + 1);
            $members = $value instanceof ParsariumObject ? $value->members : get_object_vars($value);
            foreach ($members as $child) { $walk($child, $depth + 1); }
        } elseif (is_array($value)) {
            $counts['arrays']++;
            $maxDepth = max($maxDepth, $depth + 1);
            foreach ($value as $child) { $walk($child, $depth + 1); }
        } elseif (is_bool($value)) {
            $counts['booleans']++;
        } elseif ($value === null) {
            $counts['nulls']++;
        } elseif (is_string($value)) {
            $strings[] = $value;
        } elseif (is_int($value) || is_float($value)) {
            $numbers[] = $value;
        } else {
            throw new UnexpectedValueException('unexpected decoded value type: ' . get_debug_type($value));
        }
    };
    $walk($root, 0);
    sort($numbers, SORT_NUMERIC);
    sort($strings, SORT_STRING);
    $keys = match (true) {
        $root instanceof stdClass => array_map('strval', array_keys(get_object_vars($root))),
        $root instanceof ParsariumObject => array_map('strval', array_keys($root->members)),
        default => [],
    };
    sort($keys, SORT_STRING);
    $root_kind = match (true) {
        $root instanceof stdClass, $root instanceof ParsariumObject => 'object', is_array($root) => 'array', is_string($root) => 'string',
        is_bool($root) => 'boolean', $root === null => 'null', default => 'number',
    };
    return ['arrays' => $counts['arrays'], 'booleans' => $counts['booleans'], 'max_depth' => $maxDepth,
            'nulls' => $counts['nulls'], 'numbers' => $numbers, 'objects' => $counts['objects'],
            'root' => $root_kind, 'strings' => $strings, 'top_level_keys' => $keys];
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
