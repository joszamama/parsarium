# qusql-parse — SQL / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.12.0`
- **License:** Apache-2.0
- **Parser family:** qusql-parse hand-written lexer and recursive-descent parser
- **Local input API:** `parse_statements(local UTF-8 text, &mut Issues, &ParseOptions::new()) -> Vec<Statement>`
- **Documentation:** [API reference](<https://docs.rs/qusql-parse/0.12.0/qusql_parse/fn.parse_statements.html>)
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
python3 parsarium.py build sql rust qusql_parse
python3 parsarium.py run sql rust qusql_parse controls/sql/select-join.sql
```
