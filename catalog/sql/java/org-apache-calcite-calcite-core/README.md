# org.apache.calcite:calcite-core — SQL / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.42.0`
- **License:** Apache-2.0
- **Parser family:** Apache Calcite JavaCC grammar (SqlParserImpl)
- **Local input API:** `SqlParser.create(local SQL text, SqlParser.config()).parseStmtList() -> SqlNodeList`
- **Documentation:** [API reference](<https://calcite.apache.org/javadocAggregate/org/apache/calcite/sql/parser/SqlParser.html>)
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
python3 parsarium.py build sql java calcite
python3 parsarium.py run sql java calcite controls/sql/select-join.sql
```
