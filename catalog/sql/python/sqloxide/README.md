# sqloxide — SQL / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.61.1`
- **License:** MIT
- **Parser family:** sqlparser-rs
- **Local input API:** `sqloxide.parse_sql(local SQL text, dialect="generic") -> list of statement ASTs (Python dicts)`
- **Documentation:** [API reference](<https://pypi.org/project/sqloxide/0.61.1/>)
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
python3 parsarium.py build sql python sqloxide
python3 parsarium.py run sql python sqloxide controls/sql/select-join.sql
```
