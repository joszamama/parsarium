"""antlr-tsql over local SQL text through antlr_tsql.ast.parse (T-SQL grammar, tsql_file start rule).

ast.parse runs the package's ANTLR 4 generated T-SQL lexer and parser (antlr_tsql/antlr_py) on the
antlr4 Python runtime and shapes the parse tree with antlr-ast into the package's AST node classes
(Script, Batch, SelectStmt, InsertStmt, JoinExpr, Identifier, Call, BinaryExpr, ValueList, Terminal).
Every summary field is read from that tree.

The tree does not type constants: a constant is a Terminal in an expression position whose text is
the token (for example 'paid' with its quotes, or 19.5). The adapter treats a quoted Terminal as a
string and unquotes it, and a Terminal that is a decimal number as a number, the same handling the
PHP greenlion adapter uses for its untyped 'const' nodes. Identifier parts, aliases, operators,
join kinds and INSERT column names are Terminals in named fields and are not constants.
"""

import re

from antlr_ast.ast import AST, Terminal
from antlr_tsql import ast as tsql_ast

# Fields whose Terminals are names or keywords, not constants.
NAME_FIELDS = {"table", "name", "alias", "op", "join_type", "into", "column_names", "schema",
               "database", "server"}
NUMBER = re.compile(r"[0-9]+(\.[0-9]+)?")


def _children(node):
    for field in node._fields:
        value = getattr(node, field, None)
        if value is not None:
            yield field, value


def _walk(node, field=None):
    """Yield (node, field it hangs from) for every AST node below node."""
    if isinstance(node, list):
        for item in node:
            yield from _walk(item, field)
    elif isinstance(node, AST):
        yield node, field
        if not isinstance(node, Terminal):
            for name, value in _children(node):
                yield from _walk(value, name)


def _of(node, kind: str) -> list:
    return [item for item, _ in _walk(node) if type(item).__name__ == kind]


def _literals(node) -> list[list[str]]:
    literals = []
    for item, field in _walk(node):
        if not isinstance(item, Terminal) or field in NAME_FIELDS:
            continue
        text = str(item.value)
        if len(text) >= 2 and text[0] == text[-1] == "'":
            literals.append(["string", text[1:-1].replace("''", "'")])
        elif NUMBER.fullmatch(text):
            literals.append(["number", text])
    return sorted(literals)


def _tables(node) -> list[str]:
    names = set()
    for item in _of(node, "Identifier"):
        # A relation reference is an Identifier with only its table part.
        if getattr(item, "name", None) is None and getattr(item, "table", None) is not None:
            names.add(str(item.table.value).lower())
    return sorted(names)


def summarize(statement) -> dict:
    kind = type(statement).__name__
    if kind == "SelectStmt":
        order = getattr(statement, "order_by_clause", None)
        return {"kind": "select", "tables": _tables(getattr(statement, "from_clause", None) or []),
                "select_items": len(statement.target_list or []),
                "joins": len(_of(getattr(statement, "from_clause", None) or [], "JoinExpr")),
                "where": getattr(statement, "where_clause", None) is not None,
                "group_by": len(getattr(statement, "group_by_clause", None) or []),
                "order_by": len(order.expr or []) if order is not None else 0,
                "functions": sorted({str(call.name.value).lower() for call in _of(statement, "Call")}),
                "literals": _literals(statement)}
    if kind == "InsertStmt":
        return {"kind": "insert", "tables": _tables(statement.target),
                "columns": len(statement.column_names or []),
                "rows": len(statement.values_clause or []),
                "literals": _literals(statement.values_clause or [])}
    return {"kind": kind}


def parse_sql(data: bytes) -> dict:
    if not data or len(data) > (1 << 20):
        raise ValueError("input outside harness limit")
    script = tsql_ast.parse(data.decode("utf-8"))
    statements = [statement for batch in script.batch for statement in batch.statements]
    return {"statement_count": len(statements),
            "statements": [summarize(statement) for statement in statements]}


def fuzz_one_input(data: bytes):
    try:
        parse_sql(data)
    except (ValueError, UnicodeError, tsql_ast.ParseError, RecursionError, AttributeError, TypeError):
        pass
