# @saralsql/tsql-parser — SQL / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.4.7`
- **Upstream:** [source repository](<https://github.com/saralstalin/saralsqlparser>) · [npm](<https://www.npmjs.com/package/@saralsql/tsql-parser>)
- **License:** MIT
- **Parser family:** @saralsql/tsql-parser hand-written T-SQL parser
- **Local input API:** `analyze(local UTF-8 text) -> {ast: Program, issues}`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@saralsql/tsql-parser/v/0.4.7>)
- **Valid control:** [`controls/sql/select-join.sql`](../../../../controls/sql/select-join.sql)
- **Catalog evidence:** [parser record](../../../../data/javascript/sql/parsers.json) · [control result](../../../../data/javascript/sql/verification.json)

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
python3 parsarium.py build sql javascript saralsql_tsql_parser
python3 parsarium.py run sql javascript saralsql_tsql_parser controls/sql/select-join.sql
```
