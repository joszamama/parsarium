"""pglast over local SQL text through pglast.parse_sql (libpg_query, PostgreSQL 18 grammar).

parse_sql runs libpg_query's raw parser and converts the C parse tree into
pglast.ast nodes (pglast's own Cython conversion). Every summary field is read
from those nodes (RawStmt, SelectStmt, InsertStmt, RangeVar, JoinExpr,
FuncCall, A_Const); the SQL text is never inspected directly.
"""

from pglast import ast, parse_sql as pg_parse_sql
from pglast.parser import ParseError


def _walk(node):
    if isinstance(node, ast.Node):
        yield node
        for name in node:
            yield from _walk(getattr(node, name))
    elif isinstance(node, (tuple, list)):
        for item in node:
            yield from _walk(item)


def _of(node, kind) -> list:
    return [item for item in _walk(node) if isinstance(item, kind)]


def _tables(node) -> list[str]:
    return sorted({item.relname.lower() for item in _of(node, ast.RangeVar)})


def _literals(node) -> list[list[str]]:
    literals = []
    for constant in _of(node, ast.A_Const):
        value = constant.val
        if isinstance(value, ast.String):
            literals.append(["string", value.sval])
        elif isinstance(value, ast.Integer):
            literals.append(["number", str(value.ival)])
        elif isinstance(value, ast.Float):
            literals.append(["number", value.fval])
    return sorted(literals)


def summarize(statement) -> dict:
    if isinstance(statement, ast.SelectStmt):
        return {"kind": "select", "tables": _tables(statement.fromClause),
                "select_items": len(statement.targetList or ()),
                "joins": len(_of(statement.fromClause, ast.JoinExpr)),
                "where": statement.whereClause is not None,
                "group_by": len(statement.groupClause or ()),
                "order_by": len(statement.sortClause or ()),
                "functions": sorted({call.funcname[-1].sval.lower() for call in _of(statement, ast.FuncCall)}),
                "literals": _literals(statement)}
    if isinstance(statement, ast.InsertStmt):
        values = statement.selectStmt.valuesLists if isinstance(statement.selectStmt, ast.SelectStmt) else None
        return {"kind": "insert", "tables": _tables(statement.relation),
                "columns": len(statement.cols or ()), "rows": len(values or ()),
                "literals": _literals(statement)}
    return {"kind": type(statement).__name__}


def parse_sql(data: bytes) -> dict:
    if not data or len(data) > (1 << 20):
        raise ValueError("input outside harness limit")
    statements = [raw.stmt for raw in pg_parse_sql(data.decode("utf-8"))]
    return {"statement_count": len(statements),
            "statements": [summarize(statement) for statement in statements]}


def fuzz_one_input(data: bytes):
    try:
        parse_sql(data)
    except (ValueError, UnicodeError, ParseError, RecursionError):
        pass
