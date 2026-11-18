# org.apache.shardingsphere:shardingsphere-sql-parser-engine — SQL / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `5.3.2`
- **Upstream:** [source repository](<https://github.com/apache/shardingsphere>) · [Maven Central](<https://central.sonatype.com/artifact/org.apache.shardingsphere/shardingsphere-sql-parser-engine>)
- **License:** Apache-2.0
- **Parser family:** Apache ShardingSphere ANTLR4 dialect grammars (MySQL module)
- **Local input API:** `SQLParserEngine("MySQL", CacheOption).parse(local SQL text, false) -> ParseASTNode; SQLVisitorEngine("MySQL", "STATEMENT", false, Properties).visit(tree) -> SQLStatement`
- **Documentation:** [API reference](<https://shardingsphere.apache.org/document/5.3.2/en/reference/sharding/parse/>)
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
python3 parsarium.py build sql java shardingsphere_sql_parser
python3 parsarium.py run sql java shardingsphere_sql_parser controls/sql/select-join.sql
```
