# sqllens — SQL / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.11.0`
- **Upstream:** [source repository](<https://github.com/NiclasOlofsson/sqllens>) · [npm](<https://www.npmjs.com/package/sqllens>)
- **License:** MIT
- **Parser family:** sqllens ANTLR4 grammars (PostgreSQL grammar forked from antlr/grammars-v4)
- **Local input API:** `parse(local UTF-8 text, 'postgres') -> {ast, errors, cst}`
- **Documentation:** [API reference](<https://www.npmjs.com/package/sqllens/v/1.11.0>)
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
python3 parsarium.py build sql javascript sqllens
python3 parsarium.py run sql javascript sqllens controls/sql/select-join.sql
```
