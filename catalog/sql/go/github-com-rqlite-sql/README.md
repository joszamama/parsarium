# github.com/rqlite/sql — SQL / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v0.0.0-20261016220845-5c0832fea6e1`
- **Upstream:** [source repository](<https://github.com/rqlite/sql>) · [pkg.go.dev](<https://pkg.go.dev/github.com/rqlite/sql>)
- **License:** MIT
- **Parser family:** rqlite/sql hand-written recursive-descent parser and scanner
- **Local input API:** `sql.NewParser(reader).ParseStatements() -> []sql.Statement`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/rqlite/sql@v0.0.0-20261016220845-5c0832fea6e1#Parser.ParseStatements>)
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
python3 parsarium.py build sql go github_com_rqlite_sql
python3 parsarium.py run sql go github_com_rqlite_sql controls/sql/select-join.sql
```
