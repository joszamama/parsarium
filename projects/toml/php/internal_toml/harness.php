<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';

use Internal\Toml\Node\Document;
use Internal\Toml\Node\Entry;
use Internal\Toml\Node\Table;
use Internal\Toml\Node\TableArray;
use Internal\Toml\Node\Value\ArrayValue;
use Internal\Toml\Node\Value\BooleanValue;
use Internal\Toml\Node\Value\DateTimeType;
use Internal\Toml\Node\Value\DateTimeValue;
use Internal\Toml\Node\Value\FloatValue;
use Internal\Toml\Node\Value\InlineTableValue;
use Internal\Toml\Node\Value\IntegerValue;
use Internal\Toml\Node\Value\LocalTimeValue;
use Internal\Toml\Node\Value\StringValue;
use Internal\Toml\Node\Value\Value;
use Internal\Toml\Toml;

// Shortest round-trip float digits written positionally with at least one fractional digit.
function parsarium_float(float $value): string {
    if (!is_finite($value)) { throw new UnexpectedValueException('non-finite float'); }
    $previous = ini_set('serialize_precision', '-1');
    $text = var_export($value, true);
    ini_set('serialize_precision', (string) $previous);
    if (preg_match('/^(-?)(\d)(?:\.(\d+))?E([+-]\d+)$/', $text, $m)) {
        $digits = rtrim($m[2] . ($m[3] ?? ''), '0') ?: '0';
        $point = 1 + (int) $m[4];
        if ($point <= 0) { $text = $m[1] . '0.' . str_repeat('0', -$point) . $digits; }
        elseif ($point >= strlen($digits)) { $text = $m[1] . $digits . str_repeat('0', $point - strlen($digits)) . '.0'; }
        else { $text = $m[1] . substr($digits, 0, $point) . '.' . substr($digits, $point); }
    }
    return str_contains($text, '.') ? $text : $text . '.0';
}

// Seconds plus only the significant digits of a fraction (omitted when zero).
function parsarium_seconds(DateTimeInterface $value): string {
    $fraction = rtrim($value->format('u'), '0');
    return $value->format('H:i:s') . ($fraction === '' ? '' : '.' . $fraction);
}

// Type-tags one internal/toml AST value node (the library's typed value, not the input text).
function parsarium_tag(Value $value): array|stdClass {
    return match (true) {
        $value instanceof StringValue => ['type' => 'string', 'value' => $value->value],
        $value instanceof IntegerValue => ['type' => 'integer', 'value' => (string) $value->value],
        $value instanceof FloatValue => ['type' => 'float', 'value' => parsarium_float($value->value)],
        $value instanceof BooleanValue => ['type' => 'bool', 'value' => $value->value ? 'true' : 'false'],
        $value instanceof DateTimeValue => match ($value->type) {
            DateTimeType::OffsetDatetime => ['type' => 'datetime', 'value' =>
                $value->value->setTimezone(new DateTimeZone('UTC'))->format('Y-m-d\T')
                . parsarium_seconds($value->value->setTimezone(new DateTimeZone('UTC'))) . 'Z'],
            DateTimeType::LocalDatetime => ['type' => 'datetime-local', 'value' =>
                $value->value->format('Y-m-d\T') . parsarium_seconds($value->value)],
            DateTimeType::LocalDate => ['type' => 'date-local', 'value' => $value->value->format('Y-m-d')],
        },
        // LocalTimeValue keeps the parsed local time as a typed node holding an "HH:MM:SS[.fraction]" string.
        $value instanceof LocalTimeValue => ['type' => 'time-local', 'value' => str_contains($value->value, '.')
            ? rtrim(rtrim($value->value, '0'), '.') : $value->value],
        $value instanceof ArrayValue => array_map('parsarium_tag', $value->elements),
        $value instanceof InlineTableValue => $value->pairs === [] ? new stdClass() : array_map('parsarium_tag', $value->pairs),
        default => throw new UnexpectedValueException('unexpected value node: ' . get_debug_type($value)),
    };
}

// Places Value nodes along a key path the way Document::toArray() places their PHP values.
function parsarium_place(array &$current, array $segments, Value $value): void {
    $ref = &$current;
    $last = count($segments) - 1;
    foreach ($segments as $i => $segment) {
        if ($i === $last) { $ref[$segment] = $value; }
        else { $ref[$segment] ??= []; $ref = &$ref[$segment]; }
    }
}

function parsarium_entries(array &$current, array $entries): void {
    foreach ($entries as $entry) {
        if ($entry instanceof Entry && $entry->isKeyValue()) {
            parsarium_place($current, $entry->key->segments, $entry->value);
        }
    }
}

// Walks the documented Document AST (Entry, Table and TableArray nodes) into a tree of
// Value nodes, following the table and array-of-tables placement of Document::toArray().
function parsarium_nodes(Document $document): array {
    $result = [];
    foreach ($document->nodes as $node) {
        if ($node instanceof Entry && $node->isKeyValue()) {
            parsarium_place($result, $node->key->segments, $node->value);
        } elseif ($node instanceof Table || $node instanceof TableArray) {
            $current = &$result;
            $segments = $node->name->segments;
            $last = count($segments) - 1;
            foreach ($segments as $i => $segment) {
                $current[$segment] ??= [];
                if ($node instanceof TableArray && $i === $last) {
                    $current[$segment][] = [];
                    $current = &$current[$segment][count($current[$segment]) - 1];
                } elseif (is_array($current[$segment]) && array_is_list($current[$segment]) && $current[$segment] !== []) {
                    $current = &$current[$segment][count($current[$segment]) - 1];
                } else {
                    $current = &$current[$segment];
                }
            }
            parsarium_entries($current, $node->entries);
            unset($current);
        }
    }
    return $result;
}

function parsarium_project(mixed $tree): mixed {
    return $tree instanceof Value ? $tree->toPhpValue() : array_map('parsarium_project', $tree);
}

// An empty table is an empty stdClass so it prints as {} (a PHP empty array would print as []).
function parsarium_typed(mixed $tree): array|stdClass {
    if ($tree instanceof Value) { return parsarium_tag($tree); }
    return $tree === [] ? new stdClass() : array_map('parsarium_typed', $tree);
}

// Recursively sorts table keys (TOML key order is not significant); lists keep their order.
function parsarium_canonical(mixed $tree): mixed {
    if (!is_array($tree)) { return $tree; }
    $tree = array_map('parsarium_canonical', $tree);
    if (!array_is_list($tree)) { ksort($tree, SORT_STRING); }
    return $tree;
}

function parsarium_parse(string $input): array|stdClass {
    if ($input === '' || strlen($input) > (1 << 20)) {
        throw new InvalidArgumentException('input outside harness limit');
    }
    $document = Toml::parse($input);
    $nodes = parsarium_nodes($document);
    // The AST walk must place exactly the values the library's own toArray() returns.
    if (serialize(parsarium_project($nodes)) !== serialize($document->toArray())) {
        throw new UnexpectedValueException('AST walk differs from Document::toArray()');
    }
    return parsarium_canonical(parsarium_typed($nodes));
}
