# org.jooq:jooq — SQL / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `3.21.9`
- **License:** Apache-2.0
- **Parser family:** jOOQ hand-written recursive-descent parser (ParserImpl) and query object model
- **Local input API:** `DSL.using(SQLDialect.DEFAULT).parser().parse(local SQL text) -> Queries`
- **Documentation:** [API reference](<https://www.jooq.org/doc/3.21/manual/sql-building/sql-parser/sql-parser-api/>)
- **Valid control:** [`controls/sql/select-join.sql`](../../../../controls/sql/select-join.sql)
- **Catalog evidence:** [parser record](../../../../data/java/sql/parsers.json) · [control result](../../../../data/java/sql/verification.json)

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
python3 parsarium.py build sql java jooq
python3 parsarium.py run sql java jooq controls/sql/select-join.sql
```
