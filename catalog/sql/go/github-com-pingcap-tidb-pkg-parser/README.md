# github.com/pingcap/tidb/pkg/parser — SQL / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v0.0.0-20261117145351-1e84b3595a3e`
- **Upstream:** [source repository](<https://github.com/pingcap/tidb>) · [pkg.go.dev](<https://pkg.go.dev/github.com/pingcap/tidb/pkg/parser>)
- **License:** Apache-2.0
- **Parser family:** TiDB MySQL grammar (goyacc parser.y) and lexer
- **Local input API:** `parser.New().Parse(local SQL text, "", "") -> []ast.StmtNode`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/pingcap/tidb/pkg/parser@v0.0.0-20261117145351-1e84b3595a3e#Parser.Parse>)
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
python3 parsarium.py build sql go github_com_pingcap_tidb_pkg_parser
python3 parsarium.py run sql go github_com_pingcap_tidb_pkg_parser controls/sql/select-join.sql
```
