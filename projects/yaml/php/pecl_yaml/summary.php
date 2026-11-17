<?php
declare(strict_types=1);

// The documented yaml_parse() callbacks map YAML tags to handlers; ext/yaml also applies them to implicit
// tags, so YAML_MAP_TAG (tag:yaml.org,2002:map) turns every mapping into a stdClass in source order while
// sequences stay PHP lists. Without it, {} and [] both become an empty PHP array.
function parsarium_yaml_parse(string $input): mixed {
    $documents = 0;
    $value = yaml_parse($input, 0, $documents, [YAML_MAP_TAG => static fn (array $map): stdClass => (object) $map]);
    if ($value === false || $documents !== 1) {
        throw new RuntimeException('yaml_parse did not return exactly one document');
    }
    return $value;
}

// Shortest round-trip decimal text for a PHP float (serialize_precision=-1).
function parsarium_float(float $value): string {
    return json_encode($value, JSON_THROW_ON_ERROR | JSON_PRESERVE_ZERO_FRACTION);
}

// Builds the shared YAML typed tree from the values yaml_parse returns: mappings as stdClass, sequences as lists.
function parsarium_tree(mixed $value): array {
    if ($value instanceof stdClass) {
        $members = [];
        foreach (get_object_vars($value) as $key => $item) {
            $members[] = [(string) $key, parsarium_tree($item)];
        }
        return ['map', $members];
    }
    if (is_array($value)) {
        if (!array_is_list($value)) {
            throw new UnexpectedValueException('mapping returned as a PHP array');
        }
        return ['seq', array_map('parsarium_tree', $value)];
    }
    return match (true) {
        is_string($value) => ['str', $value],
        is_int($value) => ['int', (string) $value],
        is_float($value) => ['float', parsarium_float($value)],
        is_bool($value) => ['bool', $value],
        $value === null => ['null'],
        default => throw new UnexpectedValueException('unexpected YAML value ' . get_debug_type($value)),
    };
}

function parsarium_summary(array $tree): array {
    $counts = [];
    $visit = function (array $node, int $depth) use (&$visit, &$counts): int {
        $counts[$node[0]] = ($counts[$node[0]] ?? 0) + 1;
        if ($node[0] === 'map') {
            return max([$depth, ...array_map(fn ($pair) => $visit($pair[1], $depth + 1), $node[1])]);
        }
        if ($node[0] === 'seq') {
            return max([$depth, ...array_map(fn ($item) => $visit($item, $depth + 1), $node[1])]);
        }
        return $depth - 1;
    };
    $depth = $visit($tree, 1);
    ksort($counts);
    return ['root' => $tree[0], 'nodes' => $counts, 'max_depth' => $depth, 'tree' => $tree];
}

function parsarium_parse(string $input): array {
    if ($input === '' || strlen($input) > (1 << 20)) {
        throw new InvalidArgumentException('input outside harness limit');
    }
    return parsarium_summary(parsarium_tree(parsarium_yaml_parse($input)));
}
