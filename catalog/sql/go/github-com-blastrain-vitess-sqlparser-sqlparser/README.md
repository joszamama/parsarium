# github.com/blastrain/vitess-sqlparser/sqlparser — SQL / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v0.0.0-20201030050434-a139afbb1aba`
- **License:** Apache-2.0
- **Parser family:** vitess MySQL grammar (fork, goyacc sql.y) and tokenizer; TiDB fallback for DDL only
- **Local input API:** `sqlparser.Parse(local SQL text) -> Statement`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/blastrain/vitess-sqlparser@v0.0.0-20201030050434-a139afbb1aba/sqlparser#Parse>)
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
python3 parsarium.py build sql go github_com_blastrain_vitess_sqlparser_sqlparser
python3 parsarium.py run sql go github_com_blastrain_vitess_sqlparser_sqlparser controls/sql/select-join.sql
```
