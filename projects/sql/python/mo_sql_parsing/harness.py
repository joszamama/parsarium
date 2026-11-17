"""mo-sql-parsing grammar (on the mo-parsing engine) over local SQL text through mo_sql_parsing.parse.

parse returns the documented JSON parse tree: a mapping per statement with
select/from/where/groupby/orderby or insert/values keys. Expressions are
{operator_or_function: arguments} mappings, string literals are
{"literal": text}, and numbers are Python numbers. Functions are told apart
from operators with the library's own operator precedence table
(mo_sql_parsing.keywords.precedence). The SQL text is never inspected directly.
"""

from mo_parsing.exceptions import ParseException
from mo_sql_parsing import parse
from mo_sql_parsing.keywords import precedence

STRUCTURAL = {"value", "name", "literal", "on", "using", "all_columns", "distinct"}


def _as_list(value) -> list:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def _number(value) -> list[str]:
    return ["number", str(value)]


def _expression(node, functions: set, literals: list) -> None:
    if isinstance(node, bool) or node is None:
        return
    if isinstance(node, (int, float)):
        literals.append(_number(node))
    elif isinstance(node, list):
        for item in node:
            _expression(item, functions, literals)
    elif isinstance(node, dict):
        for key, argument in node.items():
            if key == "literal":
                for text in _as_list(argument):
                    literals.append(["string", text])
                continue
            if key not in STRUCTURAL and key not in precedence:
                functions.add(key.lower())
            if key != "name":
                _expression(argument, functions, literals)


def _table(item) -> str | None:
    if isinstance(item, str):
        return item
    if isinstance(item, dict) and isinstance(item.get("value"), str):
        return item["value"]
    return None


def summarize(statement: dict) -> dict:
    if "select" in statement:
        tables, joins = set(), 0
        functions, literals = set(), []
        for item in _as_list(statement.get("from")):
            join = [key for key in item if key.endswith("join")] if isinstance(item, dict) else []
            if join:
                joins += 1
                tables.add(_table(item[join[0]]))
                _expression(item.get("on"), functions, literals)
            else:
                tables.add(_table(item))
        for key in ("select", "where", "groupby", "orderby"):
            _expression(statement.get(key), functions, literals)
        return {"kind": "select", "tables": sorted(name.lower() for name in tables if name),
                "select_items": len(_as_list(statement["select"])), "joins": joins,
                "where": "where" in statement,
                "group_by": len(_as_list(statement.get("groupby"))),
                "order_by": len(_as_list(statement.get("orderby"))),
                "functions": sorted(functions), "literals": sorted(literals)}
    if "insert" in statement:
        rows = _as_list(statement.get("values"))
        literals = []
        for row in rows:
            for value in row.values():
                literals.append(["string", value] if isinstance(value, str) else _number(value))
        return {"kind": "insert", "tables": [statement["insert"].lower()],
                "columns": len(rows[0]) if rows else 0, "rows": len(rows),
                "literals": sorted(literals)}
    return {"kind": next(iter(statement), "unknown")}


def parse_sql(data: bytes) -> dict:
    if not data or len(data) > (1 << 20):
        raise ValueError("input outside harness limit")
    tree = parse(data.decode("utf-8"))
    statements = _as_list(tree)
    return {"statement_count": len(statements),
            "statements": [summarize(statement) for statement in statements]}


def fuzz_one_input(data: bytes):
    try:
        parse_sql(data)
    except (ValueError, UnicodeError, ParseException, RecursionError):
        pass
