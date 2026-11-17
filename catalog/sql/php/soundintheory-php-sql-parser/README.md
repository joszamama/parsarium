# soundintheory/php-sql-parser — SQL / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.0`
- **License:** BSD-2-Clause
- **Parser family:** PHP-SQL-Parser lineage (2013 PSR-0 fork of the Google Code php-sql-parser; shared family with greenlion/php-sql-parser)
- **Local input API:** `(new PHPSQL\Parser())->parse(local SQL text) -> clause-keyed array parse tree`
- **Documentation:** [API reference](<https://github.com/soundintheory/php-sql-parser/blob/dcb81216a13be124d21711b8fefb6e80db7af472/README.md>)
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
python3 parsarium.py build sql php soundintheory_php_sql_parser
python3 parsarium.py run sql php soundintheory_php_sql_parser controls/sql/select-join.sql
```
