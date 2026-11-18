# phpmyadmin/sql-parser — SQL / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `6.0.1`
- **Upstream:** [source repository](<https://github.com/phpmyadmin/sql-parser>) · [Packagist](<https://packagist.org/packages/phpmyadmin/sql-parser>)
- **License:** GPL-2.0-or-later
- **Parser family:** phpMyAdmin sql-parser hand-written lexer and statement parser
- **Local input API:** `new PhpMyAdmin\SqlParser\Parser(local SQL text, strict: true) -> statements[]`
- **Documentation:** [API reference](<https://github.com/phpmyadmin/sql-parser/blob/6.0.1/README.md#parsing>)
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
python3 parsarium.py build sql php phpmyadmin_sql_parser
python3 parsarium.py run sql php phpmyadmin_sql_parser controls/sql/select-join.sql
```
