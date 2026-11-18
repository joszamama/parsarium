"""polyglot-sql over local SQL text through polyglot_sql.parse (generic dialect).

parse runs the polyglot-sql Rust tokenizer and parser (crates/polyglot-sql) through the package's
pyo3 binding and returns typed Expression objects (Select, Insert, Table, Literal, Count, Sum, ...).
Every summary field is read from that tree: the binding's Expression.walk() traversal for tables,
function calls and literals, and the Select/Insert argument records for clause counts. The SQL text
is never inspected directly.
"""

import polyglot_sql

FUNCTION_NODES = ("Function", "AggregateFunction", "Anonymous")
# Typed aggregate nodes carry the function in their key, as in the Rust polyglot-sql adapter.
TYPED_AGGREGATES = {"count", "sum", "avg", "min", "max"}


def _literals(node) -> list[list[str]]:
    literals = []
    for item in node.walk():
        if item.key == "literal":
            kind = item.args.get("literal_type")
            if kind in ("string", "number"):
                literals.append([kind, item.args["value"]])
    return sorted(literals)


def _tables(node) -> list[str]:
    return sorted({item.name.lower() for item in node.walk() if item.key == "table"})


def _functions(node) -> list[str]:
    names = set()
    for item in node.walk():
        if type(item).__name__ in FUNCTION_NODES:
            names.add(item.name.lower())
        elif item.key in TYPED_AGGREGATES:
            names.add(item.key)
    return sorted(names)


def _count(clause) -> int:
    return len(clause.get("expressions") or []) if clause else 0


def summarize(statement) -> dict:
    if statement.key == "select":
        args = statement.args
        return {"kind": "select", "tables": _tables(statement),
                "select_items": len(statement.expressions),
                "joins": len(args.get("joins") or []),
                "where": args.get("where_clause") is not None,
                "group_by": _count(args.get("group_by")),
                "order_by": _count(args.get("order_by")),
                "functions": _functions(statement),
                "literals": _literals(statement)}
    if statement.key == "insert":
        args = statement.args
        return {"kind": "insert", "tables": [args["table"]["name"]["name"].lower()],
                "columns": len(args.get("columns") or []),
                "rows": len(args.get("values") or []),
                "literals": _literals(statement)}
    return {"kind": statement.key}


def parse_sql(data: bytes) -> dict:
    if not data or len(data) > (1 << 20):
        raise ValueError("input outside harness limit")
    statements = polyglot_sql.parse(data.decode("utf-8"), dialect="generic")
    return {"statement_count": len(statements),
            "statements": [summarize(statement) for statement in statements]}


def fuzz_one_input(data: bytes):
    try:
        parse_sql(data)
    except (ValueError, UnicodeError, RecursionError, KeyError, TypeError, polyglot_sql.PolyglotError):
        pass
