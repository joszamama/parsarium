# tree-sitter-sql — SQL / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.3.11`
- **License:** MIT
- **Parser family:** tree-sitter-sql grammar on the tree-sitter C runtime
- **Local input API:** `ts_parser_new(); ts_parser_set_language(parser, tree_sitter_sql()); ts_parser_parse_string(parser, NULL, local SQL text, length) -> TSTree (concrete syntax tree; ts_node_has_error false)`
- **Documentation:** [API reference](<https://tree-sitter.github.io/tree-sitter/using-parsers/1-getting-started.html>)
- **Valid control:** [`controls/sql/select-join.sql`](../../../../controls/sql/select-join.sql)
- **Catalog evidence:** [parser record](../../../../data/c/sql/parsers.json) · [control result](../../../../data/c/sql/verification.json)

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
python3 parsarium.py build sql c tree_sitter_sql
python3 parsarium.py run sql c tree_sitter_sql controls/sql/select-join.sql
```
