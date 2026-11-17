<?php
declare(strict_types=1);
// The 2016 package emits PHP 8.5 deprecations (case-semicolon syntax, ArrayAccess return types,
// dynamic properties); they go to stderr so stdout stays the JSON summary.
ini_set('display_errors', 'stderr');
// php-fuzzer's error handler throws on every error that error_reporting() allows, and the autoloader
// compiles the deprecated package files lazily inside the fuzz target, so deprecations are not reported.
error_reporting(E_ALL & ~E_DEPRECATED);
require __DIR__ . '/vendor/autoload.php';

use SQLParser\Stmt\{Expr, ExprList, Join};

// Collects function names and literal values by walking Expr members and ExprList terms through
// the parser's public getters.
function parsarium_visit(mixed $node, array &$functions, array &$literals): void {
    if ($node instanceof ExprList) {
        foreach ($node->getExprs() as $child) { parsarium_visit($child, $functions, $literals); }
    } elseif ($node instanceof Expr) {
        if ($node->is('VALUE')) {
            $value = $node->getMember(0);
            if (is_string($value)) {
                $literals[] = ['string', $value];
            } elseif (is_int($value) || is_float($value)) {
                // The parser converts number tokens to int/float; for these controls the PHP string form
                // equals the source text (10, 19.5, 250).
                $literals[] = ['number', (string) $value];
            }
            return;
        }
        if ($node->is('CALL')) { $functions[] = strtolower((string) $node->getMember(0)); }
        foreach ($node->getMembers() as $child) { parsarium_visit($child, $functions, $literals); }
    } elseif ($node instanceof Join) {
        parsarium_visit($node->getCondition(), $functions, $literals);
    } elseif (is_array($node)) {
        foreach ($node as $child) { parsarium_visit($child, $functions, $literals); }
    }
}

function parsarium_sorted(array $values): array {
    $values = array_values(array_unique($values));
    sort($values, SORT_STRING);
    return $values;
}

function parsarium_literals(array $literals): array {
    // Byte-wise order like the oracle (PHP sort() would compare numeric strings as numbers).
    usort($literals, fn (array $a, array $b): int => strcmp($a[0], $b[0]) ?: strcmp($a[1], $b[1]));
    return $literals;
}

function parsarium_statement(object $statement): array {
    $functions = $literals = [];
    if ($statement instanceof SQL\Select) {
        $joins = $statement->hasJoins() ? $statement->getJoins() : [];
        $tables = array_values($statement->getTables());
        foreach ($joins as $join) { $tables[] = $join->getTable(); }
        $group = $statement->hasGroupBy() ? $statement->getGroupBy()->getExprs() : [];
        $order = $statement->hasOrderBy() ? $statement->getOrderBy() : [];
        $where = $statement->hasWhere() ? $statement->getWhere() : null;
        parsarium_visit([$statement->getColumns(), $joins, $where, $group, $order], $functions, $literals);
        return ['kind' => 'select', 'tables' => parsarium_sorted(array_map('strtolower', $tables)),
                'select_items' => count($statement->getColumns()), 'joins' => count($joins),
                'where' => $where !== null, 'group_by' => count($group), 'order_by' => count($order),
                'functions' => parsarium_sorted($functions), 'literals' => parsarium_literals($literals)];
    }
    if ($statement instanceof SQL\Insert) {
        $fields = $statement->hasFields() ? $statement->getFields()->getExprs() : [];
        $values = $statement->getValues();
        parsarium_visit($values, $functions, $literals);
        return ['kind' => 'insert', 'tables' => [strtolower((string) $statement->getTable())],
                'columns' => count($fields), 'rows' => is_array($values) ? count($values) : 0,
                'literals' => parsarium_literals($literals)];
    }
    return ['kind' => strtolower((new ReflectionClass($statement))->getShortName())];
}

function parsarium_parse(string $input): array {
    if ($input === '' || strlen($input) > (1 << 20)) {
        throw new InvalidArgumentException('input outside harness limit');
    }
    // SQLParser::parse returns one body entry per ';'-separated statement; the slot after the final
    // ';' is null, which is not a statement.
    $body = (new SQLParser())->parse($input);
    $statements = [];
    foreach ($body as $statement) {
        if (is_object($statement)) { $statements[] = parsarium_statement($statement); }
    }
    if ($statements === []) {
        throw new UnexpectedValueException('no statement parsed');
    }
    return ['statement_count' => count($statements), 'statements' => $statements];
}
