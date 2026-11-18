# org.apache.hive:hive-exec — SQL / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `4.2.1`
- **Upstream:** [Maven Central](<https://central.sonatype.com/artifact/org.apache.hive/hive-parser>)
- **License:** Apache-2.0
- **Parser family:** Apache Hive ANTLR3 HiveQL grammar (HiveParser)
- **Local input API:** `new ParseDriver().parse(local SQL text without its terminating semicolon).getTree() -> ASTNode`
- **Documentation:** [API reference](<https://svn.apache.org/repos/infra/websites/production/hive/content/javadocs/r4.2.1/api/org/apache/hadoop/hive/ql/parse/ParseDriver.html>)
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
python3 parsarium.py build sql java hive_exec
python3 parsarium.py run sql java hive_exec controls/sql/select-join.sql
```
