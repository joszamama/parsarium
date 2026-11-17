# sqlparse — SQL / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.6.1`
- **License:** BSD-3-Clause
- **Parser family:** sqlparse regex lexer and token-grouping engine (non-validating)
- **Local input API:** `sqlparse.parse(local SQL text) -> tuple of grouped Statement token trees`
- **Documentation:** [API reference](<https://sqlparse.readthedocs.io/en/0.6.1/api.html#sqlparse.parse>)
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
python3 parsarium.py build sql python sqlparse
python3 parsarium.py run sql python sqlparse controls/sql/select-join.sql
```
