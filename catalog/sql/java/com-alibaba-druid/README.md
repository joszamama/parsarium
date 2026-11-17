# com.alibaba:druid — SQL / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.2.28`
- **License:** Apache-2.0
- **Parser family:** Druid hand-written SQL lexer and recursive-descent parsers
- **Local input API:** `SQLUtils.parseStatements(local SQL text, DbType.mysql) -> List<SQLStatement>`
- **Documentation:** [API reference](<https://github.com/alibaba/druid/wiki/SQL-Parser>)
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
python3 parsarium.py build sql java druid
python3 parsarium.py run sql java druid controls/sql/select-join.sql
```
