# io.trino:trino-parser — SQL / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `484`
- **License:** Apache-2.0
- **Parser family:** Presto/Trino ANTLR4 SqlBase grammar (Trino branch)
- **Local input API:** `new SqlParser().createStatement(local SQL text without its terminating semicolon) -> Statement`
- **Documentation:** [API reference](<https://javadoc.io/doc/io.trino/trino-parser/484/io/trino/sql/parser/SqlParser.html>)
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
python3 parsarium.py build sql java trino_parser
python3 parsarium.py run sql java trino_parser controls/sql/select-join.sql
```
