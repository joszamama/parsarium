# spg-sql — SQL / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `9.1.0`
- **Upstream:** [source repository](<https://github.com/goliajp/spg>) · [crates.io](<https://crates.io/crates/spg-sql>)
- **License:** MIT OR Apache-2.0
- **Parser family:** spg-sql hand-written PostgreSQL-dialect lexer and recursive-descent parser
- **Local input API:** `parser::parse_statement(local UTF-8 text) -> Statement`
- **Documentation:** [API reference](<https://docs.rs/spg-sql/9.1.0/spg_sql/parser/fn.parse_statement.html>)
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
python3 parsarium.py build sql rust spg_sql
python3 parsarium.py run sql rust spg_sql controls/sql/select-join.sql
```
