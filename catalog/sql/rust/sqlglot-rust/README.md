# sqlglot-rust — SQL / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.11.2`
- **License:** MIT
- **Parser family:** sqlglot-rust tokenizer and recursive-descent parser (sqlglot-inspired)
- **Local input API:** `parser::parse_statements(local UTF-8 text, Dialect::Ansi) -> Vec<Statement>`
- **Documentation:** [API reference](<https://docs.rs/sqlglot-rust/0.11.2/sqlglot_rust/parser/fn.parse_statements.html>)
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
python3 parsarium.py build sql rust sqlglot_rust
python3 parsarium.py run sql rust sqlglot_rust controls/sql/select-join.sql
```
