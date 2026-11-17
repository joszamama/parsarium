# sqlparser — SQL / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.64.0`
- **License:** Apache-2.0
- **Parser family:** sqlparser-rs tokenizer and recursive-descent parser
- **Local input API:** `Parser::parse_sql(&GenericDialect, local UTF-8 text) -> Vec<Statement>`
- **Documentation:** [API reference](<https://docs.rs/sqlparser/0.64.0/sqlparser/parser/struct.Parser.html#method.parse_sql>)
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
python3 parsarium.py build sql rust sqlparser
python3 parsarium.py run sql rust sqlparser controls/sql/select-join.sql
```
