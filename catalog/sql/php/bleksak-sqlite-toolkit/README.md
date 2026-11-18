# bleksak/sqlite-toolkit — SQL / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.0.4`
- **Upstream:** [source repository](<https://github.com/Bleksak/sqlite-toolkit>) · [Packagist](<https://packagist.org/packages/bleksak/sqlite-toolkit>)
- **License:** MIT
- **Parser family:** bleksak/sqlite-toolkit hand-written SQLite state-machine parser (typed AST)
- **Local input API:** `(new Bleksak\SqliteToolkit\Parser())->parse(local SQL text) -> list of AST statement nodes (Ast\Select, Ast\Insert, ...)`
- **Documentation:** [API reference](<https://github.com/Bleksak/sqlite-toolkit/blob/9eef2cec4efe3efb972e6fef854333ecd9a0b8e2/docs/spec/08-parser-design.md>)
- **Valid control:** [`controls/sql/select-join.sql`](../../../../controls/sql/select-join.sql)
- **Catalog evidence:** [parser record](../../../../data/php/sql/parsers.json) · [control result](../../../../data/php/sql/verification.json)

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
python3 parsarium.py build sql php bleksak_sqlite_toolkit
python3 parsarium.py run sql php bleksak_sqlite_toolkit controls/sql/select-join.sql
```
