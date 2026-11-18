# flow-php/postgresql — SQL / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.48.0`
- **Upstream:** [source repository](<https://github.com/flow-php/postgresql>) · [Packagist](<https://packagist.org/packages/flow-php/postgresql>)
- **License:** MIT
- **Parser family:** PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser)
- **Local input API:** `Flow\PostgreSql\DSL\sql_parse(local SQL text) -> ParsedQuery over the Protobuf\AST\ParseResult tree`
- **Documentation:** [API reference](<https://flow-php.com/documentation/components/libs/postgresql/>)
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
python3 parsarium.py build sql php flow_php_postgresql
python3 parsarium.py run sql php flow_php_postgresql controls/sql/select-join.sql
```
