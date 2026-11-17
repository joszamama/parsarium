# github.com/AfterShip/clickhouse-sql-parser/parser — SQL / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v0.5.7`
- **License:** MIT
- **Parser family:** clickhouse-sql-parser hand-written recursive-descent parser and lexer
- **Local input API:** `parser.NewParser(local SQL text).ParseStmts() -> []parser.Expr`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/AfterShip/clickhouse-sql-parser@v0.5.7/parser#Parser.ParseStmts>)
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
python3 parsarium.py build sql go github_com_aftership_clickhouse_sql_parser_parser
python3 parsarium.py run sql go github_com_aftership_clickhouse_sql_parser_parser controls/sql/select-join.sql
```
