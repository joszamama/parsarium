# json-glib — JSON / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.10.8`
- **License:** LGPL-2.1-or-later
- **Parser family:** JSON-GLib JsonParser over its own JsonScanner
- **Local input API:** `json_parser_load_from_data(JsonParser *parser, const gchar *data, gssize length, GError **error) after json_parser_set_strict(parser, TRUE)`
- **Documentation:** [API reference](<https://gnome.pages.gitlab.gnome.org/json-glib/method.Parser.load_from_data.html>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/c/json/parsers.json) · [control result](../../../../data/c/json/verification.json)

## Observed control result

```json
{
  "arrays": 3,
  "booleans": 2,
  "max_depth": 4,
  "nulls": 1,
  "numbers": [
    -2.5,
    1,
    1,
    2,
    2
  ],
  "objects": 5,
  "root": "object",
  "strings": [
    "café \"quoted\"",
    "go",
    "json",
    "parsarium",
    "rfc8259"
  ],
  "top_level_keys": [
    "enabled",
    "missing",
    "name",
    "nested",
    "ratio",
    "tags",
    "version"
  ]
}
```

## Run this target

```sh
python3 parsarium.py build json c json-glib
python3 parsarium.py run json c json-glib controls/json/nested-object.json
```
