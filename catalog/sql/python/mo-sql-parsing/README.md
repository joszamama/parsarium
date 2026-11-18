# mo-sql-parsing — SQL / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `11.699.26234`
- **Upstream:** [source repository](<https://github.com/klahnakoski/mo-sql-parsing>) · [PyPI](<https://pypi.org/project/mo-sql-parsing/>)
- **License:** MPL-2.0
- **Parser family:** mo-sql-parsing grammar on the mo-parsing engine
- **Local input API:** `mo_sql_parsing.parse(local SQL text) -> JSON parse tree`
- **Documentation:** [API reference](<https://github.com/klahnakoski/mo-sql-parsing/blob/master/README.md#parsing-sql>)
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
python3 parsarium.py build sql python mo_sql_parsing
python3 parsarium.py run sql python mo_sql_parsing controls/sql/select-join.sql
```
