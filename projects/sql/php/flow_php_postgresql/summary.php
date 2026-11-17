<?php
declare(strict_types=1);

// flow-php/postgresql: the documented sql_parse(string $sql): ParsedQuery runs Parser::parse(), which calls the
// pg_query extension's pg_query_parse_protobuf() and decodes the bytes into the package's protobuf AST classes
// (Flow\PostgreSql\Protobuf\AST\*) with google/protobuf. The oracle summary is read with the package's own
// Traverser and a NodeVisitor over that typed tree, plus the statement nodes' generated getters.

require_once __DIR__ . '/vendor/autoload.php';

use Flow\PostgreSql\AST\NodeVisitor;
use Flow\PostgreSql\AST\Traverser;
use Flow\PostgreSql\ParsedQuery;
use Flow\PostgreSql\Protobuf\AST\A_Const;
use Flow\PostgreSql\Protobuf\AST\FuncCall;
use Flow\PostgreSql\Protobuf\AST\InsertStmt;
use Flow\PostgreSql\Protobuf\AST\JoinExpr;
use Flow\PostgreSql\Protobuf\AST\RangeVar;
use Flow\PostgreSql\Protobuf\AST\SelectStmt;

use function Flow\PostgreSql\DSL\sql_parse;

function parsarium_sql_parse(string $sql): ParsedQuery {
    return sql_parse($sql);
}

/** Collects one summary per top-level SelectStmt/InsertStmt; nested statements belong to the open one. */
final class ParsariumSummaryVisitor implements NodeVisitor {
    /** @var list<array{node: object, tables: array<string, true>, functions: array<string, true>, literals: list<array{0: string, 1: string}>, joins: int}> */
    public array $statements = [];
    private int $depth = 0;

    public static function nodeClasses(): array {
        return [SelectStmt::class, InsertStmt::class, RangeVar::class, JoinExpr::class, FuncCall::class, A_Const::class];
    }

    public function enter(object $node): ?int {
        if ($node instanceof SelectStmt || $node instanceof InsertStmt) {
            if ($this->depth++ === 0) {
                $this->statements[] = ['node' => $node, 'tables' => [], 'functions' => [], 'literals' => [], 'joins' => 0];
            }
            return null;
        }
        if ($this->statements === []) { return null; }
        $current = &$this->statements[count($this->statements) - 1];
        if ($node instanceof RangeVar) {
            $current['tables'][strtolower($node->getRelname())] = true;
        } elseif ($node instanceof JoinExpr) {
            $current['joins']++;
        } elseif ($node instanceof FuncCall) {
            $names = iterator_to_array($node->getFuncname(), false);
            $current['functions'][strtolower($names[count($names) - 1]->getString()->getSval())] = true;
        } elseif ($node instanceof A_Const) {
            match ($node->getVal()) {
                'sval' => $current['literals'][] = ['string', $node->getSval()->getSval()],
                'ival' => $current['literals'][] = ['number', (string) $node->getIval()->getIval()],
                'fval' => $current['literals'][] = ['number', $node->getFval()->getFval()],
                default => null,
            };
        }
        return null;
    }

    public function leave(object $node): ?int {
        if ($node instanceof SelectStmt || $node instanceof InsertStmt) { $this->depth--; }
        return null;
    }
}

function parsarium_summary(ParsedQuery $query): array {
    $visitor = new ParsariumSummaryVisitor();
    $query->traverse($visitor);
    $statements = [];
    foreach ($visitor->statements as $item) {
        $tables = array_keys($item['tables']);
        $functions = array_keys($item['functions']);
        sort($tables, SORT_STRING);
        sort($functions, SORT_STRING);
        $literals = $item['literals'];
        // Byte-wise order of [kind, text], as in the oracle (numeric strings must not compare as numbers).
        usort($literals, fn (array $a, array $b): int => strcmp($a[0], $b[0]) ?: strcmp($a[1], $b[1]));
        $node = $item['node'];
        if ($node instanceof SelectStmt) {
            $statements[] = ['kind' => 'select', 'tables' => $tables,
                             'select_items' => count($node->getTargetList()), 'joins' => $item['joins'],
                             'where' => $node->hasWhereClause(), 'group_by' => count($node->getGroupClause()),
                             'order_by' => count($node->getSortClause()), 'functions' => $functions,
                             'literals' => $literals];
        } else {
            $values = $node->getSelectStmt()?->getSelectStmt()?->getValuesLists();
            $statements[] = ['kind' => 'insert', 'tables' => [strtolower($node->getRelation()->getRelname())],
                             'columns' => count($node->getCols()), 'rows' => $values === null ? 0 : count($values),
                             'literals' => $literals];
        }
    }
    $raw = count($query->raw()->getStmts());
    if ($raw !== count($statements)) { throw new RuntimeException("unsupported statement kind among $raw statements"); }
    return ['statement_count' => count($statements), 'statements' => $statements];
}

function parsarium_parse(string $sql): array {
    return parsarium_summary(parsarium_sql_parse($sql));
}
