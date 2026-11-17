# github.com/cockroachdb/cockroachdb-parser/pkg/sql/parser — SQL / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v0.25.2`
- **License:** Apache-2.0
- **Parser family:** CockroachDB PostgreSQL-compatible grammar (official v25.2 extraction, goyacc sql.y) and scanner
- **Local input API:** `parser.Parse(local SQL text) -> statements.Statements`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/cockroachdb/cockroachdb-parser@v0.25.2/pkg/sql/parser#Parse>)
- **Valid control:** [`controls/sql/select-join.sql`](../../../../controls/sql/select-join.sql)
- **Catalog evidence:** [parser record](../../../../data/go/sql/parsers.json) · [control result](../../../../data/go/sql/verification.json)

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
python3 parsarium.py build sql go github_com_cockroachdb_cockroachdb_parser_pkg_sql_parser
python3 parsarium.py run sql go github_com_cockroachdb_cockroachdb_parser_pkg_sql_parser controls/sql/select-join.sql
```
