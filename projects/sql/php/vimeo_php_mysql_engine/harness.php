<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';

use Vimeo\MysqlEngine\Parser\{SQLLexer, SQLParser};
use Vimeo\MysqlEngine\Query\{FromClause, InsertQuery, SelectQuery};
use Vimeo\MysqlEngine\Query\Expression\{ConstantExpression, FunctionExpression};
use Vimeo\MysqlEngine\TokenType;

// Walks the parser's query objects (SelectQuery, FromClause, Expression subclasses) through their public properties.
// Each object is visited once: ORDER BY may reuse a select expression object.
function parsarium_walk(mixed $node, array &$found, SplObjectStorage $seen): void {
    if (is_array($node)) {
        foreach ($node as $child) { parsarium_walk($child, $found, $seen); }
        return;
    }
    if (!is_object($node) || !str_starts_with(get_class($node), 'Vimeo\\MysqlEngine\\Query\\') || $seen->contains($node)) {
        return;
    }
    $seen->attach($node);
    if ($node instanceof FromClause) {
        foreach ($node->tables as $index => $table) {
            if ($index > 0) { $found['joins']++; }
            if (!isset($table['subquery'])) { $found['tables'][strtolower($table['name'])] = true; }
        }
    } elseif ($node instanceof FunctionExpression) {
        $found['functions'][strtolower($node->functionName)] = true;
    } elseif ($node instanceof ConstantExpression) {
        // The parser converts numeric tokens to int or float; their string form equals the source text for the controls.
        if ($node->getType() === TokenType::STRING_CONSTANT) {
            $found['literals'][] = ['string', $node->value];
        } elseif ($node->getType() === TokenType::NUMERIC_CONSTANT) {
            $found['literals'][] = ['number', (string) $node->value];
        }
    }
    foreach (get_object_vars($node) as $child) { parsarium_walk($child, $found, $seen); }
}

function parsarium_statement(object $query): array {
    $found = ['tables' => [], 'functions' => [], 'literals' => [], 'joins' => 0];
    parsarium_walk($query, $found, new SplObjectStorage());
    $tables = array_keys($found['tables']);
    $functions = array_keys($found['functions']);
    sort($tables, SORT_STRING);
    sort($functions, SORT_STRING);
    $literals = $found['literals'];
    // Byte-wise order of [kind, text], as in the oracle (numeric strings must not compare as numbers).
    usort($literals, fn (array $a, array $b): int => strcmp($a[0], $b[0]) ?: strcmp($a[1], $b[1]));
    if ($query instanceof SelectQuery) {
        return ['kind' => 'select', 'tables' => $tables, 'select_items' => count($query->selectExpressions),
                'joins' => $found['joins'], 'where' => $query->whereClause !== null,
                'group_by' => count($query->groupBy ?? []), 'order_by' => count($query->orderBy ?? []),
                'functions' => $functions, 'literals' => $literals];
    }
    if ($query instanceof InsertQuery) {
        return ['kind' => 'insert', 'tables' => [strtolower($query->table)], 'columns' => count($query->insertColumns),
                'rows' => count($query->values), 'literals' => $literals];
    }
    return ['kind' => strtolower((new ReflectionClass($query))->getShortName())];
}

function parsarium_parse(string $sql): array {
    // SQLParser::parse() reads one statement per call and rejects a ';' terminator after INSERT or FROM. The input is
    // cut at each ';' lexeme of the package's own SQLLexer (quoted strings and comments are single lexemes), the ';'
    // itself is dropped, and whitespace-only pieces (the text after the final ';') are skipped.
    $statements = [];
    $start = 0;
    $cuts = [];
    foreach ((new SQLLexer())->lex($sql) as [$lexeme, $offset]) {
        if ($lexeme === ';') { $cuts[] = $offset; }
    }
    $cuts[] = strlen($sql);
    foreach ($cuts as $end) {
        $text = substr($sql, $start, $end - $start);
        $start = $end + 1;
        if (trim($text) === '') { continue; }
        $statements[] = parsarium_statement(SQLParser::parse($text));
    }
    return ['statement_count' => count($statements), 'statements' => $statements];
}
