# databend-common-ast — SQL / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.2.5`
- **License:** Apache-2.0
- **Parser family:** Databend SQL parser (logos tokenizer, nom/pratt combinators)
- **Local input API:** `parser::tokenize_sql(local UTF-8 text) and parser::parse_sql(&tokens, Dialect::PostgreSQL) -> (Statement, Option<String>)`
- **Documentation:** [API reference](<https://docs.rs/databend-common-ast/0.2.5/databend_common_ast/parser/fn.parse_sql.html>)
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
python3 parsarium.py build sql rust databend_common_ast
python3 parsarium.py run sql rust databend_common_ast controls/sql/select-join.sql
```
