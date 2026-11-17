<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';

use PhpMyAdmin\SqlParser\Parser;
use PhpMyAdmin\SqlParser\Statement;
use PhpMyAdmin\SqlParser\Statements\InsertStatement;
use PhpMyAdmin\SqlParser\Statements\SelectStatement;
use PhpMyAdmin\SqlParser\TokenType;

// Literals come from the parser's own token list, limited to the statement's token range.
function parsarium_literals(Parser $parser, Statement $statement): array {
    $found = [];
    for ($index = $statement->first; $index <= $statement->last; $index++) {
        $token = $parser->list->tokens[$index];
        if ($token->type === TokenType::String) {
            $found[] = ['string', (string) $token->value];
        } elseif ($token->type === TokenType::Number) {
            $found[] = ['number', $token->token];
        }
    }
    // Byte-wise order like the oracle (PHP sort() would compare numeric strings as numbers).
    usort($found, fn (array $a, array $b): int => strcmp($a[0], $b[0]) ?: strcmp($a[1], $b[1]));
    return $found;
}

function parsarium_select(Parser $parser, SelectStatement $statement): array {
    $tables = [];
    foreach ($statement->from as $expression) { $tables[] = strtolower($expression->table); }
    foreach ($statement->join ?? [] as $join) { $tables[] = strtolower($join->expr->table); }
    $tables = array_values(array_unique($tables));
    sort($tables, SORT_STRING);
    $functions = [];
    foreach ($statement->expr as $expression) {
        if ($expression->function !== null) { $functions[] = strtolower($expression->function); }
    }
    $functions = array_values(array_unique($functions));
    sort($functions, SORT_STRING);
    return ['kind' => 'select', 'tables' => $tables, 'select_items' => count($statement->expr),
            'joins' => count($statement->join ?? []), 'where' => !empty($statement->where),
            'group_by' => count($statement->group ?? []), 'order_by' => count($statement->order ?? []),
            'functions' => $functions, 'literals' => parsarium_literals($parser, $statement)];
}

function parsarium_insert(Parser $parser, InsertStatement $statement): array {
    return ['kind' => 'insert', 'tables' => [strtolower($statement->into->dest->table)],
            'columns' => count($statement->into->columns ?? []), 'rows' => count($statement->values ?? []),
            'literals' => parsarium_literals($parser, $statement)];
}

function parsarium_parse(string $input): array {
    if ($input === '' || strlen($input) > (1 << 20)) {
        throw new InvalidArgumentException('input outside harness limit');
    }
    $parser = new Parser($input, true);
    $summaries = [];
    foreach ($parser->statements as $statement) {
        $summaries[] = match (true) {
            $statement instanceof SelectStatement => parsarium_select($parser, $statement),
            $statement instanceof InsertStatement => parsarium_insert($parser, $statement),
            default => ['kind' => strtolower((new ReflectionClass($statement))->getShortName())],
        };
    }
    return ['statement_count' => count($summaries), 'statements' => $summaries];
}
