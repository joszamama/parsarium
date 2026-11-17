<?php
declare(strict_types=1);

// Shared observable summary of a decoded JSON value (stdClass objects, lists, scalars).
function parsarium_json_summary(mixed $root): array {
    $counts = ['objects' => 0, 'arrays' => 0, 'booleans' => 0, 'nulls' => 0];
    $strings = [];
    $numbers = [];
    $maxDepth = 0;
    $walk = function (mixed $value, int $depth) use (&$walk, &$counts, &$strings, &$numbers, &$maxDepth): void {
        if ($value instanceof stdClass) {
            $counts['objects']++;
            $maxDepth = max($maxDepth, $depth + 1);
            foreach (get_object_vars($value) as $child) { $walk($child, $depth + 1); }
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
    $keys = $root instanceof stdClass ? array_map('strval', array_keys(get_object_vars($root))) : [];
    sort($keys, SORT_STRING);
    $root_kind = match (true) {
        $root instanceof stdClass => 'object', is_array($root) => 'array', is_string($root) => 'string',
        is_bool($root) => 'boolean', $root === null => 'null', default => 'number',
    };
    return ['arrays' => $counts['arrays'], 'booleans' => $counts['booleans'], 'max_depth' => $maxDepth,
            'nulls' => $counts['nulls'], 'numbers' => $numbers, 'objects' => $counts['objects'],
            'root' => $root_kind, 'strings' => $strings, 'top_level_keys' => $keys];
}
