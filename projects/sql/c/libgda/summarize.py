"""Print the oracle summary of one local SQL file from libgda's GdaSqlStatement tree.

/work/replay prints, per statement, the JSON that gda_sql_statement_serialize returns
for the parsed GdaSqlStatement; this script reads only that tree (stmt_type, SELECT
fields, from.targets and from.joins, where, group_by, order_by, func, INSERT table,
fields and values). libgda keeps each expression value as its SQL text: a string
literal stays quoted ('paid'), a number is its source text, and identifiers are names.
"""
import json
import os
import re
import subprocess
import sys

NUMBER = re.compile(r"^[0-9]+(\.[0-9]+)?$")


def walk(node, visit):
    if isinstance(node, dict):
        visit(node)
        for value in node.values():
            walk(value, visit)
    elif isinstance(node, list):
        for item in node:
            walk(item, visit)


def collect(node):
    functions, literals = set(), []

    def visit(item):
        function = item.get("func")
        if isinstance(function, dict):
            functions.add(function["function_name"].lower())
        value = item.get("value")
        if isinstance(value, str) and set(item) <= {"value"}:
            if len(value) >= 2 and value[0] == "'" and value[-1] == "'":
                literals.append(["string", value[1:-1].replace("''", "'")])
            elif NUMBER.match(value):
                literals.append(["number", value])

    walk(node, visit)
    return sorted(functions), sorted(literals)


def summarize(statement):
    contents = statement["contents"]
    if statement["stmt_type"] == "SELECT":
        source = contents.get("from", {})
        tables = sorted({target["table_name"].lower() for target in source.get("targets", [])
                         if "table_name" in target})
        functions, literals = collect({key: value for key, value in contents.items()
                                       if key != "from"} | {"joins": source.get("joins", [])})
        return {"kind": "select", "tables": tables,
                "select_items": len(contents.get("fields", [])),
                "joins": len(source.get("joins", [])), "where": "where" in contents,
                "group_by": len(contents.get("group_by", [])),
                "order_by": len(contents.get("order_by", [])), "functions": functions,
                "literals": literals}
    if statement["stmt_type"] == "INSERT":
        values = contents.get("values", [])
        _, literals = collect(values)
        return {"kind": "insert", "tables": [contents["table"].lower()],
                "columns": len(contents.get("fields", [])), "rows": len(values),
                "literals": literals}
    return {"kind": statement["stmt_type"].lower()}


def summary_of_tree(tree):
    statements = [summarize(item) for item in tree]
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
