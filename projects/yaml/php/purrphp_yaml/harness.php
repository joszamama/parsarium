<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';

use Purr\Yaml\Node\AbstractNode;
use Purr\Yaml\Node\AliasNode;
use Purr\Yaml\Node\MappingNode;
use Purr\Yaml\Node\ScalarNode;
use Purr\Yaml\Node\SequenceNode;
use Purr\Yaml\Schema\CoreSchema;
use Purr\Yaml\YamlStreamSingle;

// Shortest round-trip decimal text for a PHP float (serialize_precision=-1).
function parsarium_float(float $value): string {
    return json_encode($value, JSON_THROW_ON_ERROR | JSON_PRESERVE_ZERO_FRACTION);
}

function parsarium_scalar(mixed $value): array {
    return match (true) {
        is_string($value) => ['str', $value],
        is_int($value) => ['int', (string) $value],
        is_float($value) => ['float', parsarium_float($value)],
        is_bool($value) => ['bool', $value],
        $value === null => ['null'],
        default => throw new UnexpectedValueException('unexpected YAML value ' . get_debug_type($value)),
    };
}

// Builds the shared YAML typed tree from purrphp/yaml's documented node model:
// MappingNode entries in source order, SequenceNode items, AliasNode targets (the
// anchored node itself), and scalars typed by the package's own YAML 1.2 CoreSchema.
function parsarium_tree(AbstractNode $node, CoreSchema $schema): array {
    if ($node instanceof AliasNode) {
        return parsarium_tree($node->getTarget(), $schema);
    }
    if ($node instanceof MappingNode) {
        $members = [];
        foreach ($node->getEntries() as $entry) {
            $key = $schema->resolve($entry->getKey());
            if (!is_string($key) && !is_int($key)) {
                throw new UnexpectedValueException('non-scalar or non-string mapping key');
            }
            $members[] = [(string) $key, parsarium_tree($entry->getValue(), $schema)];
        }
        return ['map', $members];
    }
    if ($node instanceof SequenceNode) {
        $items = [];
        foreach ($node->getItems() as $item) {
            $items[] = parsarium_tree($item, $schema);
        }
        return ['seq', $items];
    }
    if ($node instanceof ScalarNode) {
        return parsarium_scalar($schema->resolve($node));
    }
    throw new UnexpectedValueException('unexpected YAML node ' . get_debug_type($node));
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
    // Documented single-document entry point; it throws InvalidDocumentsCountException
    // unless the source holds exactly one document.
    $document = (new YamlStreamSingle())->fromString($input);
    return parsarium_summary(parsarium_tree($document->getRoot(), new CoreSchema()));
}
