# dt-sql-parser — SQL / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `4.6.1`
- **Upstream:** [source repository](<https://github.com/DTStack/dt-sql-parser>) · [npm](<https://www.npmjs.com/package/dt-sql-parser>)
- **License:** MIT
- **Parser family:** dt-sql-parser ANTLR4 grammars
- **Local input API:** `new MySQL().parse(local UTF-8 text, errorListener) -> ProgramContext`
- **Documentation:** [API reference](<https://www.npmjs.com/package/dt-sql-parser/v/4.6.1>)
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
python3 parsarium.py build sql javascript dt_sql_parser
python3 parsarium.py run sql javascript dt_sql_parser controls/sql/select-join.sql
```
