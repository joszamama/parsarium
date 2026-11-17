# sad_spirit/pg_builder — SQL / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v3.3.1`
- **License:** BSD-2-Clause
- **Parser family:** pg_builder hand-written PostgreSQL lexer and recursive-descent parser (typed AST)
- **Local input API:** `(new sad_spirit\pg_builder\StatementFactory())->createFromString(local SQL text) -> Statement AST`
- **Documentation:** [API reference](<https://github.com/sad-spirit/pg-builder/blob/2a1ff9bf16b014f37af1fce1c4b9db53782fe7f6/README.md>)
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
python3 parsarium.py build sql php sad_spirit_pg_builder
python3 parsarium.py run sql php sad_spirit_pg_builder controls/sql/select-join.sql
```
