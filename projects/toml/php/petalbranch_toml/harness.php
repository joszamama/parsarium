<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';

use Petalbranch\Toml\Contract\Parser\NodeInterface;
use Petalbranch\Toml\Model\Node\ArrayNode;
use Petalbranch\Toml\Model\Node\TableNode;
use Petalbranch\Toml\Model\Node\ValueNode;
use Petalbranch\Toml\Parser\Lexer;
use Petalbranch\Toml\Parser\Parser;
use Petalbranch\Toml\Type\TomlType;

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

function parsarium_string(ValueNode $node): string {
    $value = $node->getValue();
    if (!is_string($value)) { throw new UnexpectedValueException('non-string value for ' . $node->getType()->name); }
    return $value;
}

// Type-tags one petalbranch/toml ValueNode by its TomlType. Date-time nodes hold the library's own
// normalized TOML text (Parser::parseDatetime builds TomlOffsetDateTime/TomlLocalDateTime/TomlDate/
// TomlTime and stores formatToml()); the offset kind is converted from that library value to the
// UTC instant, never from the input text.
function parsarium_value(ValueNode $node): array {
    $value = $node->getValue();
    return match ($node->getType()) {
        TomlType::STRING => ['type' => 'string', 'value' => parsarium_string($node)],
        TomlType::INTEGER => is_int($value) ? ['type' => 'integer', 'value' => (string) $value]
            : throw new UnexpectedValueException('non-int integer node'),
        TomlType::FLOAT => is_float($value) ? ['type' => 'float', 'value' => parsarium_float($value)]
            : throw new UnexpectedValueException('non-float float node'),
        TomlType::BOOLEAN => is_bool($value) ? ['type' => 'bool', 'value' => $value ? 'true' : 'false']
            : throw new UnexpectedValueException('non-bool boolean node'),
        TomlType::OFFSET_DATETIME => ['type' => 'datetime', 'value' => parsarium_fraction(
            (new DateTimeImmutable(parsarium_string($node)))->setTimezone(new DateTimeZone('UTC'))
                ->format('Y-m-d\TH:i:s.u')) . 'Z'],
        TomlType::LOCAL_DATETIME => ['type' => 'datetime-local', 'value' => parsarium_string($node)],
        TomlType::LOCAL_DATE => ['type' => 'date-local', 'value' => parsarium_string($node)],
        TomlType::LOCAL_TIME => ['type' => 'time-local', 'value' => parsarium_string($node)],
        default => throw new UnexpectedValueException('unexpected value type: ' . $node->getType()->name),
    };
}

// Walks the documented node tree from Parser::parseToNode: TableNode (and InlineTableNode) entries,
// ArrayNode elements (arrays and arrays of tables) and typed ValueNode leaves.
function parsarium_typed(NodeInterface $node): array {
    if ($node instanceof TableNode) {
        $result = [];
        foreach ($node->getEntries() as $entry) { $result[$entry->key] = parsarium_typed($entry->value); }
        return $result;
    }
    if ($node instanceof ArrayNode) { return array_map('parsarium_typed', $node->getElements()); }
    if ($node instanceof ValueNode) { return parsarium_value($node); }
    throw new UnexpectedValueException('unexpected node: ' . get_debug_type($node));
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
    // Documented AST entry (README "Lossless Round-Trip"): Parser over the package Lexer.
    $root = (new Parser(new Lexer()))->parseToNode($input);
    return parsarium_canonical(parsarium_typed($root));
}
