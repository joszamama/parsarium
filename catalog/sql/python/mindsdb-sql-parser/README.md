# mindsdb-sql-parser — SQL / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.13.8`
- **Upstream:** [source repository](<https://github.com/mindsdb/mindsdb_sql_parser>) · [PyPI](<https://pypi.org/project/mindsdb-sql-parser/>)
- **License:** MIT
- **Parser family:** mindsdb_sql_parser SLY grammar
- **Local input API:** `mindsdb_sql_parser.parse_sql(sql: str) -> ASTNode`
- **Documentation:** [API reference](<https://github.com/mindsdb/mindsdb_sql_parser#how-to-use (README in the pinned sdist: parse_sql returns the abstract syntax tree)>)
- **Valid control:** [`controls/sql/select-join.sql`](../../../../controls/sql/select-join.sql)
- **Catalog evidence:** [parser record](../../../../data/python/sql/parsers.json) · [control result](../../../../data/python/sql/verification.json)

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
python3 parsarium.py build sql python mindsdb_sql_parser
python3 parsarium.py run sql python mindsdb_sql_parser controls/sql/select-join.sql
```
