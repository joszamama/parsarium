<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';

use Kwasii\LaravelSqlParser\Dialects\Dialect;
use Kwasii\LaravelSqlParser\Expressions\{Anonymous, Connector, Expression, Func, Insert, Join, Literal, Schema, Select,
    Table, Tuple, Values};

// Walks the sqlglot-style expression tree (Expression::dfs over its args) for Table, Join, Func and Literal nodes.
// And/Or are Func nodes in sqlglot's class hierarchy (Connector, Func), so connectors are not counted as calls.
function parsarium_statement(?Expression $tree): array {
    if ($tree === null) { return ['kind' => 'empty']; }
    $tables = $functions = [];
    $literals = [];
    $joins = 0;
    foreach ($tree->dfs() as $node) {
        if ($node instanceof Table) {
            $tables[strtolower($node->name())] = true;
        } elseif ($node instanceof Join) {
            $joins++;
        } elseif ($node instanceof Func && !$node instanceof Connector) {
            $functions[strtolower($node instanceof Anonymous ? $node->name() : $node::sqlName())] = true;
        } elseif ($node instanceof Literal) {
            // Literal keeps the token text: the unquoted string or the number as written.
            $literals[] = [$node->isString() ? 'string' : 'number', $node->name()];
        }
    }
    $tables = array_keys($tables);
    $functions = array_keys($functions);
    sort($tables, SORT_STRING);
    sort($functions, SORT_STRING);
    // Byte-wise order of [kind, text], as in the oracle (numeric strings must not compare as numbers).
    usort($literals, fn (array $a, array $b): int => strcmp($a[0], $b[0]) ?: strcmp($a[1], $b[1]));
    if ($tree instanceof Select) {
        $group = $tree->argExpr('group');
        $order = $tree->argExpr('order');
        return ['kind' => 'select', 'tables' => $tables, 'select_items' => count($tree->expressions()),
                'joins' => $joins, 'where' => $tree->argExpr('where') !== null,
                'group_by' => $group === null ? 0 : count($group->expressions()),
                'order_by' => $order === null ? 0 : count($order->expressions()),
                'functions' => $functions, 'literals' => $literals];
    }
    if ($tree instanceof Insert) {
        // INSERT INTO t (columns) parses as Schema(this: Table, expressions: column identifiers).
        $target = $tree->this();
        $columns = $target instanceof Schema ? count($target->expressions()) : 0;
        $source = $tree->expression();
        $rows = $source instanceof Values
            ? count(array_filter($source->expressions(), fn (mixed $row): bool => $row instanceof Tuple)) : 0;
        return ['kind' => 'insert', 'tables' => $tables, 'columns' => $columns, 'rows' => $rows, 'literals' => $literals];
    }
    return ['kind' => strtolower((new ReflectionClass($tree))->getShortName())];
}

function parsarium_parse(string $sql): array {
    // Dialect::get(null) is sqlglot's base dialect; parse() returns one tree per ';'-separated statement.
    $statements = array_map('parsarium_statement', Dialect::get(null)->parse($sql));
    return ['statement_count' => count($statements), 'statements' => $statements];
}
