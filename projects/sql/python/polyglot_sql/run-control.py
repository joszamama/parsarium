"""Replay the valid SQL control through polyglot_sql.parse and check the summary; native coverage is merged afterwards."""

import json
from pathlib import Path

from harness import parse_sql

EXPECTED = {
    "statement_count": 1,
    "statements": [{
        "kind": "select", "tables": ["customers", "orders"], "select_items": 3,
        "joins": 1, "where": True, "group_by": 1, "order_by": 1,
        "functions": ["count", "sum"], "literals": [["number", "10"], ["string", "paid"]],
    }],
}

observed = parse_sql(Path("/input/control").read_bytes())
if observed != EXPECTED:
    raise SystemExit(f"control mismatch: {observed}")
Path("/coverage/observed.json").write_text(json.dumps(observed, indent=2) + "\n")
