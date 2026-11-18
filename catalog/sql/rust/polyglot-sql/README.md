# polyglot-sql — SQL / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.14.1`
- **Upstream:** [source repository](<https://github.com/tobilg/polyglot>) · [crates.io](<https://crates.io/crates/polyglot-sql>)
- **License:** MIT
- **Parser family:** polyglot-sql tokenizer and recursive-descent parser (sqlglot-style)
- **Local input API:** `polyglot_sql::parse(local UTF-8 text, DialectType::Generic) -> Vec<Expression>`
- **Documentation:** [API reference](<https://docs.rs/polyglot-sql/0.14.1/polyglot_sql/fn.parse.html>)
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
python3 parsarium.py build sql rust polyglot_sql
python3 parsarium.py run sql rust polyglot_sql controls/sql/select-join.sql
```
