# com.facebook.presto:presto-parser — SQL / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.300`
- **Upstream:** [source repository](<https://github.com/prestodb/presto>) · [Maven Central](<https://central.sonatype.com/artifact/com.facebook.presto/presto-parser>)
- **License:** Apache-2.0
- **Parser family:** Presto/Trino ANTLR4 SqlBase grammar (Presto branch)
- **Local input API:** `SqlParser.createStatement(statement text from StatementSplitter over local SQL text, ParsingOptions with DecimalLiteralTreatment.AS_DECIMAL) -> Statement`
- **Documentation:** [API reference](<https://javadoc.io/doc/com.facebook.presto/presto-parser/0.300/com/facebook/presto/sql/parser/SqlParser.html>)
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
python3 parsarium.py build sql java presto_parser
python3 parsarium.py run sql java presto_parser controls/sql/select-join.sql
```
