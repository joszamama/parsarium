# github.com/auxten/postgresql-parser/pkg/sql/parser — SQL / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v1.0.1`
- **Upstream:** [source repository](<https://github.com/auxten/postgresql-parser>) · [pkg.go.dev](<https://pkg.go.dev/github.com/auxten/postgresql-parser/pkg/sql/parser>)
- **License:** BUSL-1.1 with Change License Apache-2.0 (Change Date 2023-04-01), with BSD-style vitess portions
- **Parser family:** CockroachDB PostgreSQL-compatible grammar (v20.1 extraction, goyacc sql.y) and scanner
- **Local input API:** `parser.Parse(local SQL text) -> parser.Statements`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/auxten/postgresql-parser@v1.0.1/pkg/sql/parser#Parse>)
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
python3 parsarium.py build sql go github_com_auxten_postgresql_parser_pkg_sql_parser
python3 parsarium.py run sql go github_com_auxten_postgresql_parser_pkg_sql_parser controls/sql/select-join.sql
```
