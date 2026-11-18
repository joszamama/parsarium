# com.github.jsqlparser:jsqlparser — SQL / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `5.4`
- **Upstream:** [source repository](<https://github.com/JSQLParser/JSqlParser>) · [Maven Central](<https://central.sonatype.com/artifact/com.github.jsqlparser/jsqlparser>)
- **License:** LGPL-2.1-only OR Apache-2.0
- **Parser family:** JSqlParser JavaCC grammar (CCJSqlParser)
- **Local input API:** `CCJSqlParserUtil.parseStatements(local SQL text) -> Statements`
- **Documentation:** [API reference](<https://jsqlparser.github.io/JSqlParser/usage.html>)
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
python3 parsarium.py build sql java jsqlparser
python3 parsarium.py run sql java jsqlparser controls/sql/select-join.sql
```
