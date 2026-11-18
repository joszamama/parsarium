"""mindsdb_sql_parser over local SQL text through mindsdb_sql_parser.parse_sql (default MindsDB dialect).

parse_sql runs the package's SLY lexer and LALR parser (mindsdb_sql_parser/lexer.py and parser.py,
on the SLY copy the distribution installs) and returns its AST objects (Select, Insert, Join,
Identifier, Function, Constant, ...). Every summary field is read from that tree; the SQL text is
never inspected directly.
"""

from mindsdb_sql_parser import ParsingException, parse_sql as mindsdb_parse_sql
from mindsdb_sql_parser.ast import Constant, Function, Identifier, Insert, Join, Select
from mindsdb_sql_parser.ast.base import ASTNode


def _walk(node):
    if isinstance(node, ASTNode):
        yield node
        for value in vars(node).values():
            yield from _walk(value)
    elif isinstance(node, (list, tuple)):
        for item in node:
            yield from _walk(item)


def _of(node, kind) -> list:
    return [item for item in _walk(node) if isinstance(item, kind)]


def _relations(node) -> list:
    """Base relations of a FROM tree: Join sides, recursively, down to identifiers."""
    if isinstance(node, Join):
        return _relations(node.left) + _relations(node.right)
    return [node] if isinstance(node, Identifier) else []


def _literals(node) -> list[list[str]]:
    literals = []
    for constant in _of(node, Constant):
        value = constant.value
        if isinstance(value, str):
            literals.append(["string", value])
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            literals.append(["number", str(value)])
    return sorted(literals)


def summarize(statement) -> dict:
    if isinstance(statement, Select):
        return {"kind": "select",
                "tables": sorted({item.parts[-1].lower() for item in _relations(statement.from_table)}),
                "select_items": len(statement.targets or ()),
                "joins": len(_of(statement.from_table, Join)),
                "where": statement.where is not None,
                "group_by": len(statement.group_by or ()),
                "order_by": len(statement.order_by or ()),
                "functions": sorted({call.op.lower() for call in _of(statement, Function)}),
                "literals": _literals(statement)}
    if isinstance(statement, Insert):
        return {"kind": "insert", "tables": [statement.table.parts[-1].lower()],
                "columns": len(statement.columns or ()), "rows": len(statement.values or ()),
                "literals": _literals(statement.values)}
    return {"kind": type(statement).__name__.lower()}


def parse_sql(data: bytes) -> dict:
    if not data or len(data) > (1 << 20):
        raise ValueError("input outside harness limit")
    # parse_sql returns one statement; the controls hold exactly one.
    statements = [mindsdb_parse_sql(data.decode("utf-8"))]
    return {"statement_count": len(statements),
            "statements": [summarize(statement) for statement in statements]}


def fuzz_one_input(data: bytes):
    try:
        parse_sql(data)
    except (ValueError, UnicodeError, ParsingException, RecursionError, AttributeError, TypeError):
        pass
