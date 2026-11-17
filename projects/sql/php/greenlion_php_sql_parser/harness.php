<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';

use PHPSQLParser\PHPSQLParser;

// Every summary field is read from the nested parse-tree array that PHPSQLParser::parse returns.
function parsarium_walk(mixed $node, callable $visit): void {
    if (!is_array($node)) { return; }
    if (isset($node['expr_type'])) { $visit($node); }
    foreach ($node as $child) { parsarium_walk($child, $visit); }
}

function parsarium_sorted(array $values): array {
    $values = array_values(array_unique($values));
    sort($values, SORT_STRING);
    return $values;
}

function parsarium_collect(array $tree): array {
    $tables = $functions = $literals = [];
    parsarium_walk($tree, function (array $node) use (&$tables, &$functions, &$literals): void {
        switch ($node['expr_type']) {
            case 'table':
                $tables[] = strtolower($node['table']);
                break;
            case 'aggregate_function':
            case 'function':
                $functions[] = strtolower($node['base_expr']);
                break;
            case 'const':
                $text = $node['base_expr'];
                if (strlen($text) >= 2 && $text[0] === "'" && $text[strlen($text) - 1] === "'") {
                    $literals[] = ['string', str_replace("''", "'", substr($text, 1, -1))];
                } elseif (is_numeric($text)) {
                    $literals[] = ['number', $text];
                }
                break;
        }
    });
    // Byte-wise order like the oracle (PHP sort() would compare numeric strings as numbers).
    usort($literals, fn (array $a, array $b): int => strcmp($a[0], $b[0]) ?: strcmp($a[1], $b[1]));
    return [parsarium_sorted($tables), parsarium_sorted($functions), $literals];
}

function parsarium_parse(string $input): array {
    if ($input === '' || strlen($input) > (1 << 20)) {
        throw new InvalidArgumentException('input outside harness limit');
    }
    $tree = (new PHPSQLParser())->parse($input);
    if (!is_array($tree) || $tree === []) {
        throw new UnexpectedValueException('no statement parsed');
    }
    [$tables, $functions, $literals] = parsarium_collect($tree);
    if (isset($tree['SELECT'])) {
        $from = $tree['FROM'] ?? [];
        $joins = count(array_filter($from, fn (array $item): bool => ($item['ref_type'] ?? false) !== false));
        $statement = ['kind' => 'select', 'tables' => $tables, 'select_items' => count($tree['SELECT']),
                      'joins' => $joins, 'where' => isset($tree['WHERE']),
                      'group_by' => count($tree['GROUP'] ?? []), 'order_by' => count($tree['ORDER'] ?? []),
                      'functions' => $functions, 'literals' => $literals];
    } elseif (isset($tree['INSERT'])) {
        $columns = 0;
        foreach ($tree['INSERT'] as $part) {
            if (($part['expr_type'] ?? '') === 'column-list') { $columns = count($part['sub_tree']); }
        }
        $rows = count(array_filter($tree['VALUES'] ?? [], fn (array $item): bool => $item['expr_type'] === 'record'));
        $statement = ['kind' => 'insert', 'tables' => $tables, 'columns' => $columns, 'rows' => $rows,
                      'literals' => $literals];
    } else {
        $statement = ['kind' => strtolower((string) array_key_first($tree))];
    }
    return ['statement_count' => 1, 'statements' => [$statement]];
}
