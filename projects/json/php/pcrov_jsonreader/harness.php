<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';

use pcrov\JsonReader\JsonReader;

// Builds a type-tagged tree from JsonReader's documented pull nodes. value() is
// read only for scalar nodes: on containers it returns objects as PHP arrays.
function parsarium_tree(JsonReader $reader): array {
    $stack = [];
    $names = [];
    $roots = [];
    $attach = function (array $node, ?string $name) use (&$stack, &$roots): void {
        if ($stack === []) { $roots[] = $node; return; }
        $top = array_key_last($stack);
        if ($stack[$top]['type'] === 'array') { $stack[$top]['items'][] = $node; return; }
        if ($name === null || property_exists($stack[$top]['members'], $name)) {
            throw new UnexpectedValueException('object member without unique name');
        }
        $stack[$top]['members']->{$name} = $node;
    };
    while ($reader->read()) {
        $type = $reader->type();
        if ($type === JsonReader::END_OBJECT || $type === JsonReader::END_ARRAY) {
            $node = array_pop($stack);
            if ($node['type'] === 'object') {
                $members = get_object_vars($node['members']);
                ksort($members, SORT_STRING);
                $node['members'] = (object) $members;
            }
            $attach($node, array_pop($names));
            continue;
        }
        if ($reader->depth() !== count($stack)) {
            throw new UnexpectedValueException('reader depth disagrees with tree depth');
        }
        if ($type === JsonReader::OBJECT || $type === JsonReader::ARRAY) {
            $stack[] = $type === JsonReader::OBJECT
                ? ['type' => 'object', 'members' => new stdClass()]
                : ['type' => 'array', 'items' => []];
            $names[] = $reader->name();
            continue;
        }
        $value = $reader->value();
        $node = match ($type) {
            JsonReader::STRING => ['type' => 'string', 'value' => $value],
            JsonReader::NUMBER => ['type' => 'number', 'value' => $value],
            JsonReader::BOOL => ['type' => 'boolean', 'value' => $value],
            JsonReader::NULL => ['type' => 'null'],
        };
        $attach($node, $reader->name());
    }
    if ($stack !== [] || count($roots) !== 1) {
        throw new UnexpectedValueException('reader did not yield exactly one complete root');
    }
    return $roots[0];
}

function parsarium_parse(string $input): array {
    if ($input === '' || strlen($input) > (1 << 20)) {
        throw new InvalidArgumentException('input outside harness limit');
    }
    $reader = new JsonReader();
    $reader->json($input);
    try {
        return parsarium_tree($reader);
    } finally {
        $reader->close();
    }
}
