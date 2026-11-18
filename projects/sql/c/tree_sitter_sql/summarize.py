"""Print the oracle summary of one local SQL file from tree-sitter-sql's syntax tree.

/work/replay prints the named nodes of the concrete syntax tree that ts_parser_parse_string
builds with tree_sitter_sql() (and fails on ERROR or MISSING nodes); this script reads only
that tree: statement, select_expression/term, relation, join, where, group_by, order_by,
invocation, insert, list, column and literal nodes.
"""
import json
import os
import subprocess
import sys

JOINS = {"join", "cross_join", "lateral_join", "lateral_cross_join"}


def named(node):
    """Named children that are not keyword tokens."""
    return [child for child in node["children"] if not child["type"].startswith("keyword_")]


def walk(node):
    yield node
    for child in node["children"]:
        yield from walk(child)


def name_of(reference):
    # object_reference: optional schema/database identifiers, then the name identifier.
    return [c for c in reference["children"] if c["field"] == "name"][-1]["text"].lower()


def literal(node):
    text = node["text"]
    if text[:1] == "'" and text[-1:] == "'":
        return ["string", text[1:-1].replace("''", "'")]
    return ["number", text]


def collect(statement):
    tables, functions, literals, joins = set(), set(), [], 0
    for node in walk(statement):
        if node["type"] == "relation" or node["type"] == "insert":
            for child in node["children"]:
                if child["type"] == "object_reference":
                    tables.add(name_of(child))
        elif node["type"] in JOINS:
            joins += 1
        elif node["type"] == "invocation":
            reference = [c for c in node["children"] if c["type"] == "object_reference"][0]
            functions.add(name_of(reference))
        elif node["type"] == "literal":
            literals.append(literal(node))
    return sorted(tables), sorted(functions), sorted(literals), joins


def summarize(statement):
    parts = {child["type"]: child for child in named(statement)}
    tables, functions, literals, joins = collect(statement)
    if "select" in parts:
        select = parts["select"]
        clauses = {child["type"]: child for child in named(parts["from"])} if "from" in parts else {}
        items = [c for c in named(select) if c["type"] == "select_expression"]
        return {"kind": "select", "tables": tables,
                "select_items": len(named(items[0])) if items else 0, "joins": joins,
                "where": "where" in clauses,
                "group_by": len(named(clauses["group_by"])) if "group_by" in clauses else 0,
                "order_by": len([c for c in named(clauses["order_by"]) if c["type"] == "order_target"])
                if "order_by" in clauses else 0,
                "functions": functions, "literals": literals}
    if "insert" in parts:
        children = parts["insert"]["children"]
        values_at = [i for i, c in enumerate(children) if c["type"] == "keyword_values"]
        rows = [c for c in children[values_at[0]:] if c["type"] == "list"] if values_at else []
        targets = [c for c in children[:values_at[0] if values_at else len(children)] if c["type"] == "list"]
        columns = [c for c in targets[0]["children"] if c["type"] == "column"] if targets else []
        return {"kind": "insert", "tables": tables, "columns": len(columns), "rows": len(rows),
                "literals": literals}
    return {"kind": named(statement)[0]["type"] if named(statement) else "empty"}


def summary_of_tree(tree):
    statements = [summarize(child) for child in tree["children"] if child["type"] == "statement"]
    return {"statement_count": len(statements), "statements": statements}


def summary_of(path):
    # The replay is coverage-instrumented; keep its profile out of the working directory.
    environment = {**os.environ, "LLVM_PROFILE_FILE": "/tmp/summary-%p.profraw"}
    output = subprocess.run(["/work/replay", path], check=True, capture_output=True,
                            text=True, env=environment).stdout
    return summary_of_tree(json.loads(output))


if __name__ == "__main__":
    if sys.argv[1] == "--tree":
        with open(sys.argv[2], encoding="utf-8") as handle:
            print(json.dumps(summary_of_tree(json.load(handle))))
    else:
        print(json.dumps(summary_of(sys.argv[1])))
