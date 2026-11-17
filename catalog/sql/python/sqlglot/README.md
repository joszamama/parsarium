# sqlglot — SQL / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `30.33.0`
- **License:** MIT
- **Parser family:** sqlglot pure-Python tokenizer and recursive-descent parser
- **Local input API:** `sqlglot.parse(local SQL text, read=None) -> list of Expression trees`
- **Documentation:** [API reference](<https://sqlglot.com/sqlglot.html#parse>)
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
python3 parsarium.py build sql python sqlglot
python3 parsarium.py run sql python sqlglot controls/sql/select-join.sql
```
