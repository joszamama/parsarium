# pgsql-ast-parser — SQL / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `12.0.2`
- **License:** MIT
- **Parser family:** pgsql-ast-parser nearley grammar and moo lexer
- **Local input API:** `parse(local UTF-8 text) -> Statement[]`
- **Documentation:** [API reference](<https://www.npmjs.com/package/pgsql-ast-parser/v/12.0.2>)
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
python3 parsarium.py build sql javascript pgsql_ast_parser
python3 parsarium.py run sql javascript pgsql_ast_parser controls/sql/select-join.sql
```
