# kwasii/laravel-sql-parser — SQL / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v0.1.0`
- **License:** MIT
- **Parser family:** sqlglot family: PHP port of sqlglot 30.21.0 (own tokenizer, recursive-descent parser and expression classes)
- **Local input API:** `Kwasii\LaravelSqlParser\Dialects\Dialect::get(null)->parse(local SQL text) -> list of Expression trees (Expressions\Select, Expressions\Insert, ...)`
- **Documentation:** [API reference](<https://github.com/kwasii1/laravel-sql-parser/blob/17aa576c47feb38ef3b66b11d0cca449730f7b96/README.md#parsing>)
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
python3 parsarium.py build sql php kwasii_laravel_sql_parser
python3 parsarium.py run sql php kwasii_laravel_sql_parser controls/sql/select-join.sql
```
