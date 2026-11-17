# sqlite3-parser — SQL / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.17.0`
- **License:** Apache-2.0/MIT
- **Parser family:** SQLite grammar (lemon-rs port of SQLite's Lemon parse.y)
- **Local input API:** `lexer::sql::Parser::new(&Bump, local bytes) and FallibleIterator::next -> Option<Cmd>`
- **Documentation:** [API reference](<https://docs.rs/sqlite3-parser/0.17.0/sqlite3_parser/lexer/sql/struct.Parser.html>)
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
python3 parsarium.py build sql rust sqlite3_parser
python3 parsarium.py run sql rust sqlite3_parser controls/sql/select-join.sql
```
