"""Print the oracle summary of one local SQL file from libpg_query's parse tree.

/work/replay prints the JSON parse tree that pg_query_parse returns; this script
reads only that tree (SelectStmt, InsertStmt, RangeVar, JoinExpr, FuncCall, A_Const).
"""
import json
import os
import subprocess
import sys


def walk(node, visit):
    if isinstance(node, dict):
        for key, value in node.items():
            visit(key, value)
            walk(value, visit)
    elif isinstance(node, list):
        for item in node:
            walk(item, visit)


def collect(node):
    tables, functions, literals, joins = set(), set(), [], 0

    def visit(key, value):
        nonlocal joins
        if key == "RangeVar":
            tables.add(value["relname"].lower())
        elif key == "JoinExpr":
            joins += 1
        elif key == "FuncCall":
            functions.add(value["funcname"][-1]["String"]["sval"].lower())
        elif key == "A_Const":
            if "sval" in value:
                literals.append(["string", value["sval"].get("sval", "")])
            elif "ival" in value:
                # libpg_query omits a zero ival from the JSON output.
                literals.append(["number", str(value["ival"].get("ival", 0))])
            elif "fval" in value:
                literals.append(["number", value["fval"]["fval"]])

    walk(node, visit)
    return sorted(tables), sorted(functions), sorted(literals), joins


def summarize(statement):
    if "SelectStmt" in statement:
        select = statement["SelectStmt"]
        tables, functions, literals, joins = collect(select)
        return {"kind": "select", "tables": tables,
                "select_items": len(select.get("targetList", [])), "joins": joins,
                "where": "whereClause" in select, "group_by": len(select.get("groupClause", [])),
                "order_by": len(select.get("sortClause", [])), "functions": functions,
                "literals": literals}
    if "InsertStmt" in statement:
        insert = statement["InsertStmt"]
        _, _, literals, _ = collect(insert)
        # InsertStmt.relation is a typed RangeVar field, serialized without a node wrapper.
        tables = [insert["relation"]["relname"].lower()]
        values = insert.get("selectStmt", {}).get("SelectStmt", {}).get("valuesLists", [])
        return {"kind": "insert", "tables": tables, "columns": len(insert.get("cols", [])),
                "rows": len(values), "literals": literals}
    return {"kind": next(iter(statement)).lower()}


def summary_of_tree(tree):
    statements = [summarize(item["stmt"]) for item in tree.get("stmts", [])]
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
