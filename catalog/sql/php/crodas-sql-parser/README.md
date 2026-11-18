# crodas/sql-parser — SQL / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v0.1.5`
- **Upstream:** [source repository](<https://github.com/crodas/SQLParser>) · [Packagist](<https://packagist.org/packages/crodas/sql-parser>)
- **License:** MIT
- **Parser family:** crodas SQLParser Lemon-generated LALR parser (SQL\Statement objects)
- **Local input API:** `(new SQLParser())->parse(local SQL text) -> SQL\Statement objects`
- **Documentation:** [API reference](<https://github.com/crodas/SQLParser/blob/a0241cb8755ed36b2a0d0812503ee71abfbe52ac/README.md>)
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
python3 parsarium.py build sql php crodas_sql_parser
python3 parsarium.py run sql php crodas_sql_parser controls/sql/select-join.sql
```
