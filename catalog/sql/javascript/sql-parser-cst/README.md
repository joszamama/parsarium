# sql-parser-cst — SQL / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.44.1`
- **License:** GPL-2.0-or-later
- **Parser family:** sql-parser-cst Peggy grammar
- **Local input API:** `parse(local UTF-8 text, {dialect: 'sqlite'}) -> Program`
- **Documentation:** [API reference](<https://www.npmjs.com/package/sql-parser-cst/v/0.44.1>)
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
python3 parsarium.py build sql javascript sql_parser_cst
python3 parsarium.py run sql javascript sql_parser_cst controls/sql/select-join.sql
```
