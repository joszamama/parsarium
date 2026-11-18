# polyglot-sql — SQL / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.14.1`
- **Upstream:** [source repository](<https://github.com/tobilg/polyglot>) · [PyPI](<https://pypi.org/project/polyglot-sql/>)
- **License:** MIT
- **Parser family:** polyglot-sql tokenizer and recursive-descent parser (sqlglot-style)
- **Local input API:** `polyglot_sql.parse(sql: str, dialect: str = "generic") -> list[Expression]`
- **Documentation:** [API reference](<https://polyglot.gh.tobilg.com (README in the pinned sdist: parse(sql, dialect) and parse_one)>)
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
python3 parsarium.py build sql python polyglot_sql
python3 parsarium.py run sql python polyglot_sql controls/sql/select-join.sql
```
