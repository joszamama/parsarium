# googlesql — SQL / C++

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2026.11.2`
- **Upstream:** [source repository](<https://github.com/google/googlesql>)
- **License:** Apache-2.0
- **Parser family:** GoogleSQL (formerly ZetaSQL) Textmapper-generated parser
- **Local input API:** `googlesql::ParseNextStatement(ParseResumeLocation over local SQL text, ParserOptions{LanguageOptions()}, &ParserOutput, &at_end_of_input) -> ParserOutput::statement() (ASTStatement tree)`
- **Documentation:** [API reference](<https://github.com/google/googlesql/blob/2026.11.2/googlesql/parser/parser.h>)
- **Valid control:** [`controls/sql/select-join.sql`](../../../../controls/sql/select-join.sql)
- **Catalog evidence:** [parser record](../../../../data/cpp/sql/parsers.json) · [control result](../../../../data/cpp/sql/verification.json)

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
python3 parsarium.py build sql cpp googlesql
python3 parsarium.py run sql cpp googlesql controls/sql/select-join.sql
```
