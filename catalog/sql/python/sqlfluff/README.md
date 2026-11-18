# sqlfluff — SQL / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `4.5.0`
- **Upstream:** [source repository](<https://github.com/sqlfluff/sqlfluff>) · [PyPI](<https://pypi.org/project/sqlfluff/>)
- **License:** MIT
- **Parser family:** sqlfluff lexer and dialect grammar matcher
- **Local input API:** `sqlfluff.parse(local SQL text, dialect="ansi") -> parse-tree record`
- **Documentation:** [API reference](<https://docs.sqlfluff.com/en/4.5.0/reference/api.html#sqlfluff.parse>)
- **Valid control:** [`controls/sql/select-join.sql`](../../../../controls/sql/select-join.sql)
- **Catalog evidence:** [parser record](../../../../data/python/sql/parsers.json) · [control result](../../../../data/python/sql/verification.json)

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
python3 parsarium.py build sql python sqlfluff
python3 parsarium.py run sql python sqlfluff controls/sql/select-join.sql
```
