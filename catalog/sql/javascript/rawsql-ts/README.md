# rawsql-ts — SQL / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.30.1`
- **Upstream:** [source repository](<https://github.com/mk3008/rawsql-ts>) · [npm](<https://www.npmjs.com/package/rawsql-ts>)
- **License:** MIT
- **Parser family:** rawsql-ts hand-written tokenizer and recursive-descent parser
- **Local input API:** `SqlParser.parseMany(local UTF-8 text) -> SimpleSelectQuery | InsertQuery []`
- **Documentation:** [API reference](<https://www.npmjs.com/package/rawsql-ts/v/0.30.1>)
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
python3 parsarium.py build sql javascript rawsql_ts
python3 parsarium.py run sql javascript rawsql_ts controls/sql/select-join.sql
```
