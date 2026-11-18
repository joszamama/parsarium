# github.com/pganalyze/pg_query_go/v6 — SQL / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v6.2.5`
- **Upstream:** [source repository](<https://github.com/pganalyze/pg_query_go>) · [pkg.go.dev](<https://pkg.go.dev/github.com/pganalyze/pg_query_go/v6>)
- **License:** BSD-3-Clause AND PostgreSQL
- **Parser family:** PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser), cgo binding
- **Local input API:** `pg_query.Parse(local SQL text) -> *pg_query.ParseResult`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/pganalyze/pg_query_go/v6@v6.2.5#Parse>)
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
python3 parsarium.py build sql go github_com_pganalyze_pg_query_go_v6
python3 parsarium.py run sql go github_com_pganalyze_pg_query_go_v6 controls/sql/select-join.sql
```
