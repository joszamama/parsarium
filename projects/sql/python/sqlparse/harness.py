"""sqlparse non-validating parser over local SQL text through sqlparse.parse.

Every summary field comes from sqlparse's grouped token tree (Statement,
IdentifierList, Identifier, Function, Where, Parenthesis, Values groups and
leaf token types); the SQL text is never inspected directly.
"""

import sqlparse
from sqlparse import sql, tokens as T


def _significant(group):
    return [token for token in group.tokens if not token.is_whitespace]


def _identifier_count(token) -> int:
    if isinstance(token, sql.IdentifierList):
        return len(list(token.get_identifiers()))
    return 1


def _functions(group) -> set[str]:
    names = set()
    for token in group.tokens:
        if isinstance(token, sql.Function):
            names.add(token.get_name().lower())
        if token.is_group:
            names |= _functions(token)
    return names


def _literals(statement) -> list[list[str]]:
    found = []
    for token in statement.flatten():
        if token.ttype in T.Literal.String.Single:
            found.append(["string", token.value[1:-1].replace("''", "'")])
        elif token.ttype in T.Literal.Number:
            found.append(["number", token.value])
    return sorted(found)


def _select(statement) -> dict:
    items = _significant(statement)
    tables, joins, where = set(), 0, False
    select_items = group_by = order_by = 0
    for index, token in enumerate(items):
        following = items[index + 1] if index + 1 < len(items) else None
        if token.ttype is T.DML and token.normalized == "SELECT":
            select_items = _identifier_count(following)
        elif token.ttype is T.Keyword and (token.normalized == "FROM" or token.normalized.endswith("JOIN")):
            if token.normalized.endswith("JOIN"):
                joins += 1
            tables.add(following.get_real_name().lower())
        elif isinstance(token, sql.Where):
            where = True
        elif token.ttype is T.Keyword and token.normalized == "GROUP BY":
            group_by = _identifier_count(following)
        elif token.ttype is T.Keyword and token.normalized == "ORDER BY":
            order_by = _identifier_count(following)
    return {"kind": "select", "tables": sorted(tables), "select_items": select_items,
            "joins": joins, "where": where, "group_by": group_by, "order_by": order_by,
            "functions": sorted(_functions(statement)), "literals": _literals(statement)}


def _insert(statement) -> dict:
    items = _significant(statement)
    target = items[items.index(next(t for t in items if t.ttype is T.Keyword and t.normalized == "INTO")) + 1]
    # sqlparse groups "orders (id, ...)" as a Function-shaped group: name plus column Parenthesis.
    if isinstance(target, sql.Function):
        table = target.get_name()
        columns = next(t for t in target.tokens if isinstance(t, sql.Parenthesis))
        column_count = _identifier_count(_significant(columns)[1])
    else:
        table, column_count = target.get_real_name(), 0
    values = next(t for t in items if isinstance(t, sql.Values))
    rows = sum(isinstance(t, sql.Parenthesis) for t in values.tokens)
    return {"kind": "insert", "tables": [table.lower()], "columns": column_count,
            "rows": rows, "literals": _literals(statement)}


def parse_sql(data: bytes) -> dict:
    if not data or len(data) > (1 << 20):
        raise ValueError("input outside harness limit")
    statements = [s for s in sqlparse.parse(data.decode("utf-8"))
                  if any(not t.is_whitespace and t.ttype is not T.Punctuation for t in s.tokens)]
    summaries = []
    for statement in statements:
        kind = statement.get_type()
        if kind == "SELECT":
            summaries.append(_select(statement))
        elif kind == "INSERT":
            summaries.append(_insert(statement))
        else:
            summaries.append({"kind": kind.lower()})
    return {"statement_count": len(summaries), "statements": summaries}


def fuzz_one_input(data: bytes):
    try:
        parse_sql(data)
    except (ValueError, UnicodeError, AttributeError, IndexError, StopIteration, RecursionError):
        pass
