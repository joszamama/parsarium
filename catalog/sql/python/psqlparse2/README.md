# psqlparse2 — SQL / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.0.17`
- **Upstream:** [source repository](<https://github.com/dani-maarouf/psqlparse2>) · [PyPI](<https://pypi.org/project/psqlparse2/>)
- **License:** BSD-3-Clause
- **Parser family:** PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser)
- **Local input API:** `psqlparse2.query_to_pb(sql: str) -> psqlparse2.pb.pg_query_pb2.ParseResult`
- **Documentation:** [API reference](<https://github.com/dani-maarouf/psqlparse2#overview (README: query_to_pb / pb_to_query over pg_query_parse_protobuf)>)
- **Valid control:** [`controls/sql/select-join.sql`](../../../../controls/sql/select-join.sql)
- **Catalog evidence:** [parser record](../../../../data/python/sql/parsers.json) · [control result](../../../../data/python/sql/verification.json)

## Observed control result

```json
{
  "statement_count": 1,
  "statements": [
    {
      "kind": "select",
      "tables": [
        "customers",
        "orders"
      ],
      "select_items": 3,
      "joins": 1,
      "where": true,
      "group_by": 1,
      "order_by": 1,
      "functions": [
        "count",
        "sum"
      ],
      "literals": [
        [
          "number",
          "10"
        ],
        [
          "string",
          "paid"
        ]
      ]
    }
  ]
}
```

## Run this target

```sh
python3 parsarium.py build sql python psqlparse2
python3 parsarium.py run sql python psqlparse2 controls/sql/select-join.sql
```
