<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';

use Bleksak\SqliteToolkit\Ast\{AbstractAstNode, Call, FloatLiteral, FromSource, Insert, IntegerLiteral, Join, Select,
    SingleSelect, StringLiteral, ValuesSource};
use Bleksak\SqliteToolkit\Parser;

// Walks the typed AST through its public constructor-promoted properties, collecting base tables (FromSource names),
// Join nodes, Call names and literal nodes. Literal nodes keep the source text of numbers.
function parsarium_walk(mixed $node, array &$found): void {
    if (is_array($node)) {
        foreach ($node as $child) { parsarium_walk($child, $found); }
        return;
    }
    if (!$node instanceof AbstractAstNode) { return; }
    if ($node instanceof FromSource && $node->name !== null && $node->select === null && $node->funcArgs === []) {
        $found['tables'][strtolower($node->name->text)] = true;
    } elseif ($node instanceof Join) {
        $found['joins']++;
    } elseif ($node instanceof Call) {
        $found['functions'][strtolower($node->name->text)] = true;
    } elseif ($node instanceof StringLiteral) {
        $found['literals'][] = ['string', $node->value];
    } elseif ($node instanceof IntegerLiteral || $node instanceof FloatLiteral) {
        $found['literals'][] = ['number', $node->value];
    }
    foreach (get_object_vars($node) as $child) { parsarium_walk($child, $found); }
}

function parsarium_statement(AbstractAstNode $statement): array {
    $found = ['tables' => [], 'functions' => [], 'literals' => [], 'joins' => 0];
    parsarium_walk($statement, $found);
    $tables = array_keys($found['tables']);
    $functions = array_keys($found['functions']);
    sort($tables, SORT_STRING);
    sort($functions, SORT_STRING);
    $literals = $found['literals'];
    // Byte-wise order of [kind, text], as in the oracle (numeric strings must not compare as numbers).
    usort($literals, fn (array $a, array $b): int => strcmp($a[0], $b[0]) ?: strcmp($a[1], $b[1]));
    if ($statement instanceof Select && $statement->body instanceof SingleSelect) {
        $body = $statement->body;
        return ['kind' => 'select', 'tables' => $tables, 'select_items' => count($body->items),
                'joins' => $found['joins'], 'where' => $body->where !== null, 'group_by' => count($body->groupBy),
                'order_by' => count($body->orderBy), 'functions' => $functions, 'literals' => $literals];
    }
    if ($statement instanceof Insert) {
        $rows = $statement->source instanceof ValuesSource ? count($statement->source->rows) : 0;
        return ['kind' => 'insert', 'tables' => [strtolower($statement->table->text)],
                'columns' => count($statement->columns), 'rows' => $rows, 'literals' => $literals];
    }
    return ['kind' => strtolower((new ReflectionClass($statement))->getShortName())];
}

function parsarium_parse(string $sql): array {
    // Parser::parse() returns one statement node per ';'-terminated statement.
    $statements = array_map('parsarium_statement', (new Parser())->parse($sql));
    return ['statement_count' => count($statements), 'statements' => $statements];
}
