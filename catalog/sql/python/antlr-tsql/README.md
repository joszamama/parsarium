# antlr-tsql — SQL / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.12.6`
- **Upstream:** [source repository](<https://github.com/datacamp/antlr-tsql>) · [PyPI](<https://pypi.org/project/antlr-tsql/>)
- **License:** AGPL-3.0
- **Parser family:** antlr-tsql ANTLR 4 T-SQL grammar with antlr-ast tree shaping
- **Local input API:** `antlr_tsql.ast.parse(sql_text: str) -> Script`
- **Documentation:** [API reference](<https://github.com/datacamp/antlr-tsql#set-up-the-python-module (README in the pinned sdist: from antlr_tsql import ast; ast.parse(...))>)
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
python3 parsarium.py build sql python antlr_tsql
python3 parsarium.py run sql python antlr_tsql controls/sql/select-join.sql
```
