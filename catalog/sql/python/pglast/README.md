# pglast — SQL / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `8.8`
- **Upstream:** [source repository](<https://github.com/lelit/pglast>) · [PyPI](<https://pypi.org/project/pglast/>)
- **License:** GPL-3.0-or-later
- **Parser family:** PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser)
- **Local input API:** `pglast.parse_sql(local SQL text) -> tuple of pglast.ast.RawStmt nodes`
- **Documentation:** [API reference](<https://pglast.readthedocs.io/en/v8/parser.html#pglast.parser.parse_sql>)
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
python3 parsarium.py build sql python pglast
python3 parsarium.py run sql python pglast controls/sql/select-join.sql
```
