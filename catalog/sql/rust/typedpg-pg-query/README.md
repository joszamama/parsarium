# typedpg_pg_query — SQL / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.7.3`
- **Upstream:** [source repository](<https://github.com/cubos/typedpg>) · [crates.io](<https://crates.io/crates/typedpg_pg_query>)
- **License:** MIT AND BSD-3-Clause AND PostgreSQL
- **Parser family:** PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser)
- **Local input API:** `typedpg_pg_query::parse(local UTF-8 text) -> ParseResult`
- **Documentation:** [API reference](<https://docs.rs/typedpg_pg_query/0.7.3/typedpg_pg_query/fn.parse.html>)
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
python3 parsarium.py build sql rust typedpg_pg_query
python3 parsarium.py run sql rust typedpg_pg_query controls/sql/select-join.sql
```
