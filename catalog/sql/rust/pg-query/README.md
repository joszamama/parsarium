# pg_query — SQL / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `18.1.0`
- **Upstream:** [source repository](<https://github.com/pganalyze/pg_query.rs>) · [crates.io](<https://crates.io/crates/pg_query>)
- **License:** MIT
- **Parser family:** PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser)
- **Local input API:** `pg_query::parse(local UTF-8 text, ParserOptions::DEFAULT) -> ParseResult`
- **Documentation:** [API reference](<https://docs.rs/pg_query/18.1.0/pg_query/fn.parse.html>)
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
python3 parsarium.py build sql rust pg_query
python3 parsarium.py run sql rust pg_query controls/sql/select-join.sql
```
