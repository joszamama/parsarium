# node-sql-parser — SQL / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `5.4.0`
- **License:** Apache-2.0
- **Parser family:** node-sql-parser PEG.js grammars (one generated parser per database)
- **Local input API:** `new Parser().astify(local UTF-8 text, {database: 'postgresql'}) from node-sql-parser/build/postgresql`
- **Documentation:** [API reference](<https://www.npmjs.com/package/node-sql-parser/v/5.4.0>)
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
python3 parsarium.py build sql javascript node_sql_parser
python3 parsarium.py run sql javascript node_sql_parser controls/sql/select-join.sql
```
