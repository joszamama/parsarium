# greenlion/php-sql-parser — SQL / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v5.0.0`
- **License:** BSD-3-Clause
- **Parser family:** PHP-SQL-Parser lexer and clause processors (nested array parse tree)
- **Local input API:** `(new PHPSQLParser\PHPSQLParser())->parse(local SQL text) -> clause-keyed array parse tree`
- **Documentation:** [API reference](<https://github.com/greenlion/PHP-SQL-Parser/blob/7a4701b71f7786e8518a9412f3c552ae4550d314/README.md>)
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
python3 parsarium.py build sql php greenlion_php_sql_parser
python3 parsarium.py run sql php greenlion_php_sql_parser controls/sql/select-join.sql
```
