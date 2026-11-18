# vimeo/php-mysql-engine — SQL / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.7.15`
- **Upstream:** [source repository](<https://github.com/vimeo/php-mysql-engine>) · [Packagist](<https://packagist.org/packages/vimeo/php-mysql-engine>)
- **License:** MIT
- **Parser family:** vimeo/php-mysql-engine hand-written MySQL parser (port of Slack hack-sql-fake)
- **Local input API:** `Vimeo\MysqlEngine\Parser\SQLParser::parse(local SQL text of one statement) -> SelectQuery | InsertQuery | UpdateQuery | ... query object`
- **Documentation:** [API reference](<https://github.com/vimeo/php-mysql-engine/blob/780c49d233834dc91d5b5624c0a709080e238682/src/Parser/SQLParser.php>)
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
python3 parsarium.py build sql php vimeo_php_mysql_engine
python3 parsarium.py run sql php vimeo_php_mysql_engine controls/sql/select-join.sql
```
