<?php
declare(strict_types=1);

// flow-php/pg-query-ext: pg_query_parse(string $sql): string returns libpg_query's JSON parse tree. The bytes go to
// that one documented call; the oracle summary is read from the decoded tree only (SelectStmt, InsertStmt, RangeVar,
// JoinExpr, FuncCall, A_Const), the same fields as the C libpg_query path's summarize.py.

function parsarium_pg_query_parse(string $sql): string {
    if (!extension_loaded('pg_query')) { throw new RuntimeException('pg_query extension is not loaded'); }
    return pg_query_parse($sql);
}

function parsarium_walk(mixed $node, callable $visit): void {
    if (!is_array($node)) { return; }
    foreach ($node as $key => $value) {
        if (is_string($key)) { $visit($key, $value); }
        parsarium_walk($value, $visit);
    }
}

/** @return array{0: list<string>, 1: list<string>, 2: list<array{0: string, 1: string}>, 3: int} */
function parsarium_collect(array $node): array {
    $tables = [];
    $functions = [];
    $literals = [];
    $joins = 0;
    parsarium_walk($node, function (string $key, mixed $value) use (&$tables, &$functions, &$literals, &$joins): void {
        if (!is_array($value)) { return; }
        if ($key === 'RangeVar') {
            $tables[strtolower($value['relname'])] = true;
        } elseif ($key === 'JoinExpr') {
            $joins++;
        } elseif ($key === 'FuncCall') {
            $name = $value['funcname'][count($value['funcname']) - 1]['String']['sval'];
            $functions[strtolower($name)] = true;
        } elseif ($key === 'A_Const') {
            if (isset($value['sval'])) {
                $literals[] = ['string', (string) ($value['sval']['sval'] ?? '')];
            } elseif (isset($value['ival'])) {
                // libpg_query omits a zero ival from its JSON output.
                $literals[] = ['number', (string) ($value['ival']['ival'] ?? 0)];
            } elseif (isset($value['fval'])) {
                $literals[] = ['number', (string) $value['fval']['fval']];
            }
        }
    });
    $tables = array_keys($tables);
    $functions = array_keys($functions);
    sort($tables, SORT_STRING);
    sort($functions, SORT_STRING);
    // Byte-wise order of [kind, text], as in the oracle (numeric strings must not compare as numbers).
    usort($literals, fn (array $a, array $b): int => strcmp($a[0], $b[0]) ?: strcmp($a[1], $b[1]));
    return [$tables, $functions, $literals, $joins];
}

function parsarium_statement(array $statement): array {
    if (isset($statement['SelectStmt'])) {
        $select = $statement['SelectStmt'];
        [$tables, $functions, $literals, $joins] = parsarium_collect($select);
        return ['kind' => 'select', 'tables' => $tables,
                'select_items' => count($select['targetList'] ?? []), 'joins' => $joins,
                'where' => array_key_exists('whereClause', $select),
                'group_by' => count($select['groupClause'] ?? []),
                'order_by' => count($select['sortClause'] ?? []),
                'functions' => $functions, 'literals' => $literals];
    }
    if (isset($statement['InsertStmt'])) {
        $insert = $statement['InsertStmt'];
        [, , $literals] = parsarium_collect($insert);
        // InsertStmt.relation is a typed RangeVar field, serialized without a node wrapper.
        $values = $insert['selectStmt']['SelectStmt']['valuesLists'] ?? [];
        return ['kind' => 'insert', 'tables' => [strtolower($insert['relation']['relname'])],
                'columns' => count($insert['cols'] ?? []), 'rows' => count($values), 'literals' => $literals];
    }
    return ['kind' => strtolower((string) array_key_first($statement))];
}

function parsarium_parse(string $sql): array {
    $tree = json_decode(parsarium_pg_query_parse($sql), true, 4096, JSON_THROW_ON_ERROR);
    $statements = [];
    foreach ($tree['stmts'] ?? [] as $item) { $statements[] = parsarium_statement($item['stmt']); }
    return ['statement_count' => count($statements), 'statements' => $statements];
}
