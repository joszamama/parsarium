# libgda — SQL / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `5.2.10`
- **Upstream:** [source repository](<https://gitlab.gnome.org/GNOME/libgda>) · [Debian](<https://tracker.debian.org/pkg/libgda5>)
- **License:** LGPL-2.0-or-later
- **Parser family:** libgda Lemon-generated SQL grammar
- **Local input API:** `gda_sql_parser_parse_string(GdaSqlParser*, local NUL-terminated SQL text, &remain, &error) -> GdaStatement ("structure": GdaSqlStatement tree)`
- **Documentation:** [API reference](<libgda-5.2.10.tar.xz: doc/C/html/GdaSqlParser.html (gda_sql_parser_parse_string) and doc/C/html/libgda-5.0-GdaSqlStatement.html (GdaSqlStatement, gda_sql_statement_serialize)>)
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
python3 parsarium.py build sql c libgda
python3 parsarium.py run sql c libgda controls/sql/select-join.sql
```
