"""sqlfluff lexer and dialect grammar over local SQL text through sqlfluff.parse (ansi dialect).

sqlfluff.parse returns the parse tree as a nested record: every segment is a
one-key mapping {segment_type: value}, where value is the raw text of a leaf,
a mapping of uniquely typed children, or a list of one-key child mappings.
Every summary field is read from those segment types (select_statement,
select_clause_element, join_clause, where_clause, groupby_clause,
orderby_clause, function_name_identifier, table_reference, values_clause,
quoted_literal, numeric_literal, ...); the SQL text is never inspected directly.
"""

import sqlfluff
from sqlfluff.api.simple import APIParsingError
from sqlfluff.core.errors import SQLBaseError

NOISE = {"whitespace", "newline", "comma", "keyword", "start_bracket", "end_bracket", "dot"}


def _children(value) -> list[tuple[str, object]]:
    if isinstance(value, dict):
        return list(value.items())
    if isinstance(value, list):
        return [item for child in value for item in child.items()]
    return []


def _walk(kind: str, value):
    yield kind, value
    for child_kind, child_value in _children(value):
        yield from _walk(child_kind, child_value)


def _find(value, kind: str) -> list:
    return [found for found_kind, found in _walk("", value) if found_kind == kind]


def _text(value) -> str:
    if isinstance(value, str):
        return value
    return "".join(_text(child) for _, child in _children(value))


def _keys(value) -> int:
    """Grouping or ordering keys: children of the clause other than keywords and punctuation."""
    return sum(1 for kind, _ in _children(value) if kind not in NOISE)


def _tables(value) -> list[str]:
    names = set()
    for reference in _find(value, "table_reference"):
        parts = [child for kind, child in _children(reference) if kind == "naked_identifier"] \
            if not isinstance(reference, str) else [reference]
        names.add(parts[-1].lower())
    return sorted(names)


def _literals(value) -> list[list[str]]:
    literals = [["string", text[1:-1]] for text in _find(value, "quoted_literal")]
    literals += [["number", text] for text in _find(value, "numeric_literal")]
    return sorted(literals)


def summarize(kind: str, value) -> dict:
    if kind == "select_statement":
        return {"kind": "select", "tables": _tables(value),
                "select_items": len(_find(value, "select_clause_element")),
                "joins": len(_find(value, "join_clause")),
                "where": bool(_find(value, "where_clause")),
                "group_by": sum(_keys(clause) for clause in _find(value, "groupby_clause")),
                "order_by": sum(_keys(clause) for clause in _find(value, "orderby_clause")),
                "functions": sorted({_text(name).lower() for name in _find(value, "function_name_identifier")}),
                "literals": _literals(value)}
    if kind == "insert_statement":
        children = _children(value)
        target = next(index for index, (child, _) in enumerate(children) if child == "table_reference")
        columns = next((len(_find(child, "column_reference")) for name, child in children[target + 1:]
                        if name == "bracketed"), 0)
        rows = sum(sum(1 for name, _ in _children(clause) if name == "bracketed")
                   for clause in _find(value, "values_clause"))
        return {"kind": "insert", "tables": _tables(dict([children[target]])), "columns": columns,
                "rows": rows, "literals": _literals(value)}
    return {"kind": kind}


def parse_sql(data: bytes) -> dict:
    if not data or len(data) > (1 << 20):
        raise ValueError("input outside harness limit")
    record = sqlfluff.parse(data.decode("utf-8"), dialect="ansi")
    statements = []
    for statement in _find(record["file"], "statement"):
        statements.extend(_children(statement))
    return {"statement_count": len(statements),
            "statements": [summarize(kind, value) for kind, value in statements]}


def fuzz_one_input(data: bytes):
    try:
        parse_sql(data)
    except (ValueError, UnicodeError, APIParsingError, SQLBaseError, RecursionError):
        pass
