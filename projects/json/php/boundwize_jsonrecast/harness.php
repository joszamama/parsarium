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
        $members = new stdClass();
        foreach ($node->items as $item) {
            $name = $item->key->value;
            if (property_exists($members, $name)) {
                throw new UnexpectedValueException('duplicate object member name');
            }
            $members->{$name} = parsarium_tree($item->value);
        }
        return ['type' => 'object', 'members' => $members];
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
