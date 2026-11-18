# flow-php/pg-query-ext — SQL / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.48.0`
- **Upstream:** [source repository](<https://github.com/flow-php/pg-query-ext>) · [Packagist](<https://packagist.org/packages/flow-php/pg-query-ext>)
- **License:** MIT
- **Parser family:** PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser)
- **Local input API:** `pg_query_parse(string $sql): string -> libpg_query JSON parse tree`
- **Documentation:** [API reference](<https://flow-php.com/documentation/components/extensions/pg-query-ext/>)
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
python3 parsarium.py build sql php flow_php_pg_query_ext
python3 parsarium.py run sql php flow_php_pg_query_ext controls/sql/select-join.sql
```
