"""Check the SQL controls against hand-written summaries and SQLite's compiler.

The expected summaries in expected.json are written by hand from the statement
text; no parser under test produced them. This script checks three things:

1. Each control file has its pinned SHA-256 and is plain ASCII with LF endings.
2. Each expected summary is internally consistent with the statement text
   (every literal and table name occurs in it, counts are positive integers).
3. SQLite, through the Python standard library's in-process ``sqlite3``
   binding, compiles each statement with ``sqlite3_prepare`` (``EXPLAIN``
   prefix, so the statement is prepared but never executed) against an empty
   in-memory schema that declares the referenced tables. An authorizer callback
   records the tables and SQL functions that SQLite's own compiler resolves;
   they must equal the hand-written ``tables`` and ``functions`` values.

Limits: SQLite is one dialect. Its acceptance shows the controls are within a
subset SQLite understands; it does not prove that every dialect accepts them.
The column, join, grouping and literal counts are checked only against the
hand-written oracle, not derived from SQLite. No data is inserted or read.
"""

from hashlib import sha256
import json
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parent
CONTROLS = {
    "select-join.sql": "331b604d98d4d6c553e86b0fdc866c3c415260df7f1f59c5c2c71d1dfc7be3ca",
    "insert-values.sql": "df8f5805de6eb11bd431411bb8642e95b5a53c13c37306a6bd38ad9edf5c8c35",
}
SCHEMA = """
CREATE TABLE customers (id INTEGER PRIMARY KEY, region TEXT NOT NULL);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL,
                     total NUMERIC NOT NULL, status TEXT NOT NULL);
"""


def sqlite_resolution(statement: str) -> dict:
    connection = sqlite3.connect(":memory:")
    connection.executescript(SCHEMA)
    tables: set[str] = set()
    functions: set[str] = set()
    kinds: set[str] = set()

    def authorize(action, arg1, arg2, _database, _trigger):
        if action == sqlite3.SQLITE_READ and arg1:
            tables.add(arg1.lower())
        elif action == sqlite3.SQLITE_INSERT:
            tables.add(arg1.lower())
            kinds.add("insert")
        elif action == sqlite3.SQLITE_SELECT:
            kinds.add("select")
        elif action == sqlite3.SQLITE_FUNCTION:
            functions.add(arg2.lower())
        return sqlite3.SQLITE_OK

    connection.set_authorizer(authorize)
    # EXPLAIN makes sqlite3_prepare compile the statement into a VDBE program
    # that is listed instead of run; the target tables stay empty.
    connection.execute("EXPLAIN " + statement.strip().rstrip(";")).fetchall()
    connection.set_authorizer(None)
    rows = connection.execute("SELECT count(*) FROM orders").fetchone()[0]
    connection.close()
    if rows:
        raise SystemExit("EXPLAIN must not execute the statement")
    return {"tables": sorted(tables), "functions": sorted(functions),
            "kind": "insert" if "insert" in kinds else "select" if "select" in kinds else None,
            "sqlite_version": sqlite3.sqlite_version}


def main() -> None:
    expected = json.loads((ROOT / "expected.json").read_text())
    if set(expected["controls"]) != set(CONTROLS):
        raise SystemExit("expected.json must describe exactly the pinned controls")
    report = {}
    for name, digest in CONTROLS.items():
        data = (ROOT / name).read_bytes()
        if sha256(data).hexdigest() != digest:
            raise SystemExit(f"{name}: SHA-256 mismatch")
        if not data.isascii() or b"\r" in data or b"\t" in data or not data.endswith(b";\n"):
            raise SystemExit(f"{name}: control must be ASCII, LF-only, one terminated statement")
        text = data.decode("ascii")
        if not sqlite3.complete_statement(text) or text.count(";") != 1:
            raise SystemExit(f"{name}: must hold exactly one complete statement")
        summary = expected["controls"][name]
        if summary["statement_count"] != 1 or len(summary["statements"]) != 1:
            raise SystemExit(f"{name}: one statement expected")
        statement = summary["statements"][0]
        lower = text.lower()
        for table in statement["tables"]:
            if table not in lower:
                raise SystemExit(f"{name}: table {table} not in text")
        for kind, value in statement["literals"]:
            token = f"'{value}'" if kind == "string" else value
            if kind not in {"string", "number"} or token not in text:
                raise SystemExit(f"{name}: literal {kind} {value} not in text")
        if statement["literals"] != sorted(statement["literals"]):
            raise SystemExit(f"{name}: literals must be sorted")
        resolved = sqlite_resolution(text)
        if (resolved["kind"] != statement["kind"] or resolved["tables"] != statement["tables"]
                or resolved["functions"] != statement.get("functions", [])):
            raise SystemExit(f"{name}: SQLite resolution {resolved} differs from oracle")
        report[name] = {"sha256": digest, "bytes": len(data), "sqlite": resolved,
                        "summary": summary}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
