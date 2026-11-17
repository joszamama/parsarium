<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';

use sad_spirit\pg_builder\{BlankWalker, Insert, Lexer, Select, StatementFactory, TokenType, Values, nodes};

// Collects summary fields while pg_builder's own BlankWalker visits every node of the parsed statement.
final class ParsariumWalker extends BlankWalker {
    public array $tables = [];
    public array $functions = [];
    public array $literals = [];
    public int $joins = 0;

    public function walkRelationReference(nodes\range\RelationReference $rangeItem): mixed {
        $this->tables[] = strtolower($rangeItem->name->relation->value);
        return parent::walkRelationReference($rangeItem);
    }

    public function walkInsertTarget(nodes\range\InsertTarget $target): mixed {
        $this->tables[] = strtolower($target->relation->relation->value);
        return parent::walkInsertTarget($target);
    }

    public function walkJoinExpression(nodes\range\JoinExpression $rangeItem): mixed {
        $this->joins++;
        return parent::walkJoinExpression($rangeItem);
    }

    public function walkFunctionCall(nodes\FunctionCall $node): mixed {
        $this->functions[] = strtolower($node->name->relation->value);
        return parent::walkFunctionCall($node);
    }

    public function walkNumericConstant(nodes\expressions\NumericConstant $node): mixed {
        $this->literals[] = ['number', $node->value];
        return null;
    }

    public function walkStringConstant(nodes\expressions\StringConstant $node): mixed {
        $this->literals[] = ['string', $node->value];
        return null;
    }
}

function parsarium_sorted(array $values): array {
    $values = array_values(array_unique($values));
    sort($values, SORT_STRING);
    return $values;
}

// StatementFactory::createFromString parses exactly one statement and rejects a terminator, so the
// input is cut at the ';' special-character tokens that pg_builder's own Lexer reports.
function parsarium_statements(string $input): array {
    $stream = (new Lexer())->tokenize($input);
    $pieces = [];
    $start = 0;
    while (!$stream->isEOF()) {
        $token = $stream->next();
        if ($token->matches(TokenType::SPECIAL_CHAR, ';')) {
            $pieces[] = substr($input, $start, $token->getPosition() - $start);
            $start = $token->getPosition() + 1;
        }
    }
    $pieces[] = substr($input, $start);
    return array_values(array_filter($pieces, fn (string $piece): bool => trim($piece) !== ''));
}

function parsarium_statement(StatementFactory $factory, string $text): array {
    $statement = $factory->createFromString($text);
    $walker = new ParsariumWalker();
    $statement->dispatch($walker);
    $literals = $walker->literals;
    // Byte-wise order like the oracle (PHP sort() would compare numeric strings as numbers).
    usort($literals, fn (array $a, array $b): int => strcmp($a[0], $b[0]) ?: strcmp($a[1], $b[1]));
    $tables = parsarium_sorted($walker->tables);
    if ($statement instanceof Select) {
        return ['kind' => 'select', 'tables' => $tables, 'select_items' => count($statement->list),
                'joins' => $walker->joins, 'where' => $statement->where->condition !== null,
                'group_by' => count($statement->group), 'order_by' => count($statement->order),
                'functions' => parsarium_sorted($walker->functions), 'literals' => $literals];
    }
    if ($statement instanceof Insert) {
        $rows = $statement->values instanceof Values ? count($statement->values->rows) : 0;
        return ['kind' => 'insert', 'tables' => $tables, 'columns' => count($statement->cols), 'rows' => $rows,
                'literals' => $literals];
    }
    return ['kind' => strtolower((new ReflectionClass($statement))->getShortName())];
}

function parsarium_parse(string $input): array {
    if ($input === '' || strlen($input) > (1 << 20)) {
        throw new InvalidArgumentException('input outside harness limit');
    }
    $factory = new StatementFactory();
    $statements = [];
    foreach (parsarium_statements($input) as $text) {
        $statements[] = parsarium_statement($factory, $text);
    }
    if ($statements === []) {
        throw new UnexpectedValueException('no statement parsed');
    }
    return ['statement_count' => count($statements), 'statements' => $statements];
}
