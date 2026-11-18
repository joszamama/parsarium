"""psqlparse2 over local SQL text through psqlparse2.query_to_pb (libpg_query 16-5.1.0, PostgreSQL 16 grammar).

query_to_pb passes the text to psqlparse2's Cython wrapper (pg_query.query_parse_protobuf,
which calls libpg_query's pg_query_parse_protobuf) and decodes the bytes into the package's
generated psqlparse2.pb.pg_query_pb2.ParseResult message. Every summary field is read from that
protobuf tree (RawStmt, SelectStmt, InsertStmt, RangeVar, JoinExpr, FuncCall, A_Const); the SQL
text is never inspected directly.
"""

from google.protobuf.message import DecodeError, Message

import pg_query
from psqlparse2 import query_to_pb


def _unwrap(message: Message) -> Message:
    if message.DESCRIPTOR.name == "Node":
        which = message.WhichOneof("node")
        return getattr(message, which) if which else message
    return message


def _walk(message: Message):
    message = _unwrap(message)
    yield message
    for field, value in message.ListFields():
        if field.message_type is None:
            continue
        if field.label == field.LABEL_REPEATED:
            for item in value:
                yield from _walk(item)
        else:
            yield from _walk(value)


def _of(message, kind: str) -> list:
    if message is None:
        return []
    return [item for item in _walk(message) if item.DESCRIPTOR.name == kind]


def _tables(message) -> list[str]:
    return sorted({item.relname.lower() for item in _of(message, "RangeVar")})


def _literals(message) -> list[list[str]]:
    literals = []
    for constant in _of(message, "A_Const"):
        which = constant.WhichOneof("val")
        if which == "sval":
            literals.append(["string", constant.sval.sval])
        elif which == "ival":
            literals.append(["number", str(constant.ival.ival)])
        elif which == "fval":
            literals.append(["number", constant.fval.fval])
    return sorted(literals)


def _functions(message) -> list[str]:
    names = set()
    for call in _of(message, "FuncCall"):
        last = _unwrap(call.funcname[-1])
        names.add(last.sval.lower())
    return sorted(names)


def summarize(statement: Message) -> dict:
    kind = statement.DESCRIPTOR.name
    if kind == "SelectStmt":
        return {"kind": "select",
                "tables": sorted({t for item in statement.from_clause for t in _tables(item)}),
                "select_items": len(statement.target_list),
                "joins": sum(len(_of(item, "JoinExpr")) for item in statement.from_clause),
                "where": statement.HasField("where_clause"),
                "group_by": len(statement.group_clause),
                "order_by": len(statement.sort_clause),
                "functions": _functions(statement),
                "literals": _literals(statement)}
    if kind == "InsertStmt":
        body = _unwrap(statement.select_stmt)
        rows = len(body.values_lists) if body.DESCRIPTOR.name == "SelectStmt" else 0
        return {"kind": "insert", "tables": _tables(statement.relation),
                "columns": len(statement.cols), "rows": rows,
                "literals": _literals(statement)}
    return {"kind": kind}


def parse_sql(data: bytes) -> dict:
    if not data or len(data) > (1 << 20):
        raise ValueError("input outside harness limit")
    result = query_to_pb(data.decode("utf-8"))
    statements = [_unwrap(raw.stmt) for raw in result.stmts]
    return {"statement_count": len(statements),
            "statements": [summarize(statement) for statement in statements]}


def fuzz_one_input(data: bytes):
    try:
        parse_sql(data)
    except (ValueError, UnicodeError, pg_query.PgQueryExc, DecodeError, RecursionError):
        pass
