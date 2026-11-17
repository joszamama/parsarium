<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';

use PhpCollective\Toml\Ast\Document;
use PhpCollective\Toml\Ast\KeyValue;
use PhpCollective\Toml\Ast\Table;
use PhpCollective\Toml\Ast\Value\ArrayValue;
use PhpCollective\Toml\Ast\Value\BoolValue;
use PhpCollective\Toml\Ast\Value\FloatValue;
use PhpCollective\Toml\Ast\Value\InlineTable;
use PhpCollective\Toml\Ast\Value\IntegerValue;
use PhpCollective\Toml\Ast\Value\LocalDate;
use PhpCollective\Toml\Ast\Value\LocalDateTime;
use PhpCollective\Toml\Ast\Value\LocalTime;
use PhpCollective\Toml\Ast\Value\OffsetDateTime;
use PhpCollective\Toml\Ast\Value\StringValue;
use PhpCollective\Toml\Ast\Value\Value;
use PhpCollective\Toml\Toml;

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

// Drops trailing fractional zeros (and the point when the fraction is zero).
function parsarium_fraction(string $text): string {
    return str_contains($text, '.') ? rtrim(rtrim($text, '0'), '.') : $text;
}

// Type-tags one php-collective/toml AST value node (the library's typed value, not the input text).
function parsarium_tag(Value $value): array {
    return match (true) {
        $value instanceof StringValue => ['type' => 'string', 'value' => $value->getValue()],
        $value instanceof IntegerValue => ['type' => 'integer', 'value' => (string) $value->getValue()],
        $value instanceof FloatValue => ['type' => 'float', 'value' => parsarium_float($value->getValue())],
        $value instanceof BoolValue => ['type' => 'bool', 'value' => $value->getValue() ? 'true' : 'false'],
        $value instanceof OffsetDateTime => ['type' => 'datetime', 'value' => parsarium_fraction(
            $value->getValue()->setTimezone(new DateTimeZone('UTC'))->format('Y-m-d\TH:i:s.u')) . 'Z'],
        // The local kinds are separate typed nodes holding the library's normalized string.
        $value instanceof LocalDateTime => ['type' => 'datetime-local', 'value' => parsarium_fraction($value->getValue())],
        $value instanceof LocalDate => ['type' => 'date-local', 'value' => $value->getValue()],
        $value instanceof LocalTime => ['type' => 'time-local', 'value' => parsarium_fraction($value->getValue())],
        $value instanceof ArrayValue => array_map('parsarium_tag', $value->items),
        $value instanceof InlineTable => parsarium_typed(parsarium_inline($value)),
        default => throw new UnexpectedValueException('unexpected value node: ' . get_debug_type($value)),
    };
}

// Nests an inline table's KeyValue items by key parts, as InlineTable::getValue() does.
function parsarium_inline(InlineTable $table): array {
    $result = [];
    foreach ($table->items as $item) { parsarium_place($result, $item->key->parts, $item->value); }
    return $result;
}

function parsarium_place(array &$current, array $parts, Value $value): void {
    $ref = &$current;
    $last = count($parts) - 1;
    foreach ($parts as $i => $part) {
        if ($i === $last) { $ref[$part] = $value; }
        else { $ref[$part] ??= []; $ref = &$ref[$part]; }
    }
}

// Walks the documented Document AST (KeyValue and Table items, Table::$isArrayTable) into a
// tree of Value nodes; arrays of tables are lists and later headers extend their last element.
function parsarium_nodes(Document $document): array {
    $result = [];
    foreach ($document->items as $item) {
        if ($item instanceof KeyValue) {
            parsarium_place($result, $item->key->parts, $item->value);
            continue;
        }
        if (!$item instanceof Table) { throw new UnexpectedValueException('unexpected document item'); }
        $current = &$result;
        $parts = $item->key->parts;
        $last = count($parts) - 1;
        foreach ($parts as $i => $part) {
            $current[$part] ??= [];
            if ($item->isArrayTable && $i === $last) {
                $current[$part][] = [];
                $current = &$current[$part][count($current[$part]) - 1];
            } elseif (is_array($current[$part]) && array_is_list($current[$part]) && $current[$part] !== []) {
                $current = &$current[$part][count($current[$part]) - 1];
            } else {
                $current = &$current[$part];
            }
        }
        foreach ($item->items as $pair) { parsarium_place($current, $pair->key->parts, $pair->value); }
        unset($current);
    }
    return $result;
}

function parsarium_project(mixed $tree): mixed {
    return $tree instanceof Value ? $tree->getValue() : array_map('parsarium_project', $tree);
}

function parsarium_typed(mixed $tree): array {
    return $tree instanceof Value ? parsarium_tag($tree) : array_map('parsarium_typed', $tree);
}

// Recursively sorts table keys (TOML key order is not significant); lists keep their order.
function parsarium_canonical(mixed $tree): mixed {
    if (!is_array($tree)) { return $tree; }
    $tree = array_map('parsarium_canonical', $tree);
    if (!array_is_list($tree)) { ksort($tree, SORT_STRING); }
    return $tree;
}

function parsarium_parse(string $input): array {
    if ($input === '' || strlen($input) > (1 << 20)) {
        throw new InvalidArgumentException('input outside harness limit');
    }
    // tryParse() runs the same Parser and Normalizer as decode() and returns both the AST and
    // the normalized array; any diagnostic rejects the document as decode() would.
    $result = Toml::tryParse($input);
    if (!$result->isValid()) {
        throw new UnexpectedValueException('rejected: ' . $result->getErrors()[0]->message);
    }
    $nodes = parsarium_nodes($result->getDocument());
    // The AST walk must place exactly the values the library's own normalizer returns.
    if (serialize(parsarium_project($nodes)) !== serialize($result->getValue())) {
        throw new UnexpectedValueException('AST walk differs from the normalized value');
    }
    return parsarium_canonical(parsarium_typed($nodes));
}
