# nom-sql — SQL / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.0.11`
- **License:** MIT
- **Parser family:** nom-sql nom combinator parser (MySQL subset)
- **Local input API:** `parse_query_bytes(local bytes) -> SqlQuery`
- **Documentation:** [API reference](<https://docs.rs/nom-sql/0.0.11/nom_sql/fn.parse_query_bytes.html>)
- **Valid control:** [`controls/sql/select-join.sql`](../../../../controls/sql/select-join.sql)
- **Catalog evidence:** [parser record](../../../../data/rust/sql/parsers.json) · [control result](../../../../data/rust/sql/verification.json)

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
python3 parsarium.py build sql rust nom_sql
python3 parsarium.py run sql rust nom_sql controls/sql/select-join.sql
```
