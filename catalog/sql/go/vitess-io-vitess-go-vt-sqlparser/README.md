# vitess.io/vitess/go/vt/sqlparser — SQL / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v0.24.5`
- **License:** Apache-2.0
- **Parser family:** vitess MySQL grammar (goyacc sql.y) and tokenizer
- **Local input API:** `sqlparser.New(sqlparser.Options{}); Parser.SplitStatementToPieces and Parser.Parse(local SQL text) -> Statement`
- **Documentation:** [API reference](<https://pkg.go.dev/vitess.io/vitess@v0.24.5/go/vt/sqlparser#Parser.Parse>)
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
python3 parsarium.py build sql go vitess_io_vitess_go_vt_sqlparser
python3 parsarium.py run sql go vitess_io_vitess_go_vt_sqlparser controls/sql/select-join.sql
```
