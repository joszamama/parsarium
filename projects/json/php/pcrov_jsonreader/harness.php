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
        if ($name === null || array_key_exists($name, $stack[$top]['members'])) {
            throw new UnexpectedValueException('object member without unique name');
        }
        $stack[$top]['members'][$name] = $node;
    };
    while ($reader->read()) {
        $type = $reader->type();
        if ($type === JsonReader::END_OBJECT || $type === JsonReader::END_ARRAY) {
            $node = array_pop($stack);
            if ($node['type'] === 'object') {
                ksort($node['members'], SORT_STRING);
                $node['members'] = parsarium_members($node['members']);
            }
            $attach($node, array_pop($names));
            continue;
        }
        if ($reader->depth() !== count($stack)) {
            throw new UnexpectedValueException('reader depth disagrees with tree depth');
        }
        if ($type === JsonReader::OBJECT || $type === JsonReader::ARRAY) {
            $stack[] = $type === JsonReader::OBJECT
                ? ['type' => 'object', 'members' => []]
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
