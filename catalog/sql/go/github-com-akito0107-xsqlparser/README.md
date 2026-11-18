# github.com/akito0107/xsqlparser — SQL / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v1.0.0`
- **Upstream:** [source repository](<https://github.com/akito0107/xsqlparser>) · [pkg.go.dev](<https://pkg.go.dev/github.com/akito0107/xsqlparser>)
- **License:** Apache-2.0
- **Parser family:** xsqlparser recursive-descent parser and tokenizer (Go port of early sqlparser-rs)
- **Local input API:** `xsqlparser.NewParser(reader, &dialect.GenericSQLDialect{}).ParseSQL() -> []sqlast.Stmt`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/akito0107/xsqlparser@v1.0.0#Parser.ParseSQL>)
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
python3 parsarium.py build sql go github_com_akito0107_xsqlparser
python3 parsarium.py run sql go github_com_akito0107_xsqlparser controls/sql/select-join.sql
```
