# org.apache.spark:spark-catalyst_2.12 — SQL / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `3.5.9`
- **Upstream:** [source repository](<https://github.com/apache/spark>) · [Maven Central](<https://central.sonatype.com/artifact/org.apache.spark/spark-catalyst_2.12>)
- **License:** Apache-2.0
- **Parser family:** Spark SQL ANTLR4 SqlBase grammar (AstBuilder to unresolved LogicalPlan)
- **Local input API:** `CatalystSqlParser.parsePlan(local SQL text) -> LogicalPlan`
- **Documentation:** [API reference](<https://javadoc.io/doc/org.apache.spark/spark-catalyst_2.12/3.5.9/org/apache/spark/sql/catalyst/parser/CatalystSqlParser$.html>)
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
python3 parsarium.py build sql java spark_catalyst
python3 parsarium.py run sql java spark_catalyst controls/sql/select-join.sql
```
