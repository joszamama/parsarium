# duckdb — SQL / C++

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.0.0`
- **Upstream:** [source repository](<https://github.com/duckdb/duckdb>) · [Debian](<https://tracker.debian.org/pkg/duckdb>)
- **License:** MIT
- **Parser family:** DuckDB PEG parser (own grammar and transformer)
- **Local input API:** `duckdb::Parser::GetBuiltinParser(); Parser::ParseQuery(local SQL text) -> Parser::statements (SQLStatement trees)`
- **Documentation:** [API reference](<https://github.com/duckdb/duckdb/blob/v2.0.0/src/include/duckdb/parser/parser.hpp>)
- **Valid control:** [`controls/sql/select-join.sql`](../../../../controls/sql/select-join.sql)
- **Catalog evidence:** [parser record](../../../../data/cpp/sql/parsers.json) · [control result](../../../../data/cpp/sql/verification.json)

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
python3 parsarium.py build sql cpp duckdb
python3 parsarium.py run sql cpp duckdb controls/sql/select-join.sql
```
