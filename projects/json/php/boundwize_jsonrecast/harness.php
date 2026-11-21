<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';

use Boundwize\JsonRecast\JsonRecast;
use Boundwize\JsonRecast\Node\ArrayNode;
use Boundwize\JsonRecast\Node\BooleanNode;
use Boundwize\JsonRecast\Node\NodeJson;
use Boundwize\JsonRecast\Node\NullNode;
use Boundwize\JsonRecast\Node\NumberNode;
use Boundwize\JsonRecast\Node\ObjectNode;
use Boundwize\JsonRecast\Node\StringNode;

// Builds a type-tagged tree from JsonRecast's AST nodes, members in source order.
function parsarium_tree(NodeJson $node): array {
    if ($node instanceof ObjectNode) {
        $members = [];
        foreach ($node->items as $item) {
            $name = $item->key->value;
            if (array_key_exists($name, $members)) {
                throw new UnexpectedValueException('duplicate object member name');
            }
            $members[$name] = parsarium_tree($item->value);
        }
        return ['type' => 'object', 'members' => parsarium_members($members)];
    }
    return match (true) {
        $node instanceof ArrayNode => ['type' => 'array',
            'items' => array_map(fn ($item) => parsarium_tree($item->value), $node->items)],
        $node instanceof StringNode => ['type' => 'string', 'value' => $node->value],
        $node instanceof NumberNode => ['type' => 'number', 'value' => $node->toIntOrFloat()],
        $node instanceof BooleanNode => ['type' => 'boolean', 'value' => $node->value],
        $node instanceof NullNode => ['type' => 'null'],
        default => throw new UnexpectedValueException('unexpected AST node ' . $node::class),
    };
}

function parsarium_parse(string $input): array {
    if ($input === '' || strlen($input) > (1 << 20)) {
        throw new InvalidArgumentException('input outside harness limit');
    }
    return parsarium_tree(JsonRecast::parse($input)->value);
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
