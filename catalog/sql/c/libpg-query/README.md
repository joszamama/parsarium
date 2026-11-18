# libpg_query — SQL / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `18.1.0`
- **Upstream:** [source repository](<https://github.com/pganalyze/libpg_query>) · [Debian](<https://tracker.debian.org/pkg/libpg-query>)
- **License:** BSD-3-Clause
- **Parser family:** PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser)
- **Local input API:** `pg_query_parse(local NUL-terminated SQL text) -> PgQueryParseResult (JSON parse tree)`
- **Documentation:** [API reference](<https://github.com/pganalyze/libpg_query/blob/18.1.0/README.md#usage-parsing-a-query>)
- **Valid control:** [`controls/sql/select-join.sql`](../../../../controls/sql/select-join.sql)
- **Catalog evidence:** [parser record](../../../../data/c/sql/parsers.json) · [control result](../../../../data/c/sql/verification.json)

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
python3 parsarium.py build sql c libpg_query
python3 parsarium.py run sql c libpg_query controls/sql/select-join.sql
```
