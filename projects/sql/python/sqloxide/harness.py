"""sqloxide over local SQL text through sqloxide.parse_sql (sqlparser-rs, generic dialect).

parse_sql runs sqlparser-rs's Parser::parse_sql and returns the serde form of
the statement list as Python objects (pythonize). Every summary field is read
from that AST (Query/Select, TableWithJoins, Table, Function, Value, Insert
and Values nodes); the SQL text is never inspected directly.
"""

import sqloxide


def _walk(node):
    yield node
    if isinstance(node, dict):
        for value in node.values():
            yield from _walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from _walk(value)


def _name(parts: list) -> str:
    last = parts[-1]
    return (last.get("Identifier", last))["value"]


def _tables(node) -> list[str]:
    return sorted({_name(item["Table"]["name"]).lower() for item in _walk(node)
                   if isinstance(item, dict) and isinstance(item.get("Table"), dict)
                   and "name" in item["Table"]})


def _literals(node) -> list[list[str]]:
    literals = []
    for item in _walk(node):
        if isinstance(item, dict) and isinstance(item.get("Value"), dict) and "value" in item["Value"]:
            value = item["Value"]["value"]
            if isinstance(value, dict) and "Number" in value:
                literals.append(["number", value["Number"][0]])
            elif isinstance(value, dict) and "SingleQuotedString" in value:
                literals.append(["string", value["SingleQuotedString"]])
    return sorted(literals)


def summarize(statement: dict) -> dict:
    if "Query" in statement and "Select" in statement["Query"]["body"]:
        query = statement["Query"]
        select = query["body"]["Select"]
        group = select.get("group_by") or {}
        order = (query.get("order_by") or {}).get("kind") or {}
        return {"kind": "select", "tables": _tables(select["from"]),
                "select_items": len(select["projection"]),
                "joins": sum(len(item.get("joins") or []) for item in select["from"]),
                "where": select.get("selection") is not None,
                "group_by": len(group["Expressions"][0]) if "Expressions" in group else 0,
                "order_by": len(order.get("Expressions") or []),
                "functions": sorted({_name(item["Function"]["name"]).lower() for item in _walk(select)
                                     if isinstance(item, dict) and isinstance(item.get("Function"), dict)}),
                "literals": _literals(select)}
    if "Insert" in statement:
        insert = statement["Insert"]
        values = (insert.get("source") or {}).get("body", {}).get("Values") or {}
        table = insert["table"]
        return {"kind": "insert", "tables": [_name(table["TableName"]).lower()],
                "columns": len(insert.get("columns") or []), "rows": len(values.get("rows") or []),
                "literals": _literals(insert)}
    return {"kind": next(iter(statement)).lower()}


def parse_sql(data: bytes) -> dict:
    if not data or len(data) > (1 << 20):
        raise ValueError("input outside harness limit")
    statements = sqloxide.parse_sql(data.decode("utf-8"), dialect="generic")
    return {"statement_count": len(statements),
            "statements": [summarize(statement) for statement in statements]}


def fuzz_one_input(data: bytes):
    try:
        parse_sql(data)
    except (ValueError, UnicodeError, RecursionError):
        pass
