"""sqlglot tokenizer and parser over local SQL text through sqlglot.parse (default dialect).

Every summary field comes from sqlglot's Expression tree (exp.Select, exp.Insert,
exp.Table, exp.Join, exp.Func, exp.Literal, ...); the SQL text is never
inspected directly.
"""

import sqlglot
from sqlglot import exp


def _literals(node) -> list[list[str]]:
    return sorted(["string" if literal.is_string else "number", literal.this]
                  for literal in node.find_all(exp.Literal))


def _tables(node) -> list[str]:
    return sorted({table.name.lower() for table in node.find_all(exp.Table)})


def _count(node) -> int:
    return len(node.expressions) if node is not None else 0


def summarize(statement) -> dict:
    if isinstance(statement, exp.Select):
        return {"kind": "select", "tables": _tables(statement),
                "select_items": len(statement.expressions),
                "joins": len(statement.args.get("joins") or []),
                "where": statement.args.get("where") is not None,
                "group_by": _count(statement.args.get("group")),
                "order_by": _count(statement.args.get("order")),
                "functions": sorted({function.sql_name().lower()
                                     for function in statement.find_all(exp.Func)
                                     # AND/OR connectors and operators are Func subclasses too.
                                     if not isinstance(function, (exp.Connector, exp.Binary, exp.Unary))}),
                "literals": _literals(statement)}
    if isinstance(statement, exp.Insert):
        target = statement.this
        columns = len(target.expressions) if isinstance(target, exp.Schema) else 0
        values = statement.expression
        rows = len(values.expressions) if isinstance(values, exp.Values) else 0
        return {"kind": "insert", "tables": _tables(target), "columns": columns,
                "rows": rows, "literals": _literals(statement)}
    return {"kind": statement.key}


def parse_sql(data: bytes) -> dict:
    if not data or len(data) > (1 << 20):
        raise ValueError("input outside harness limit")
    statements = [s for s in sqlglot.parse(data.decode("utf-8"), read=None) if s is not None]
    return {"statement_count": len(statements),
            "statements": [summarize(statement) for statement in statements]}


def fuzz_one_input(data: bytes):
    try:
        parse_sql(data)
    except (ValueError, UnicodeError, sqlglot.errors.SqlglotError, RecursionError):
        pass
