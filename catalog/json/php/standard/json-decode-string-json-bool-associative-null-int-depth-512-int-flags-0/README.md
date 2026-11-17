# json_decode(string $json, ?bool $associative = null, int $depth = 512, int $flags = 0) — JSON / PHP

**Pilot / incomplete format cell.**

- **Runtime:** PHP 8.5.12 CLI (source build, --disable-all; ext/json is always enabled)
- **Parser family:** PHP ext/json re2c scanner and Bison parser
- **Official documentation:** [reference](https://www.php.net/manual/en/function.json-decode.php)
- **Valid control:** [`controls/json/nested-object.json`](../../../../../controls/json/nested-object.json)
- **Inventory:** [standard API record](../../../../../data/php/json/standard.json) · [saved result](../../../../../projects/json/php/stdlib_json_decode/verification.json)

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
python3 parsarium.py build json php stdlib_json_decode
python3 parsarium.py run json php stdlib_json_decode controls/json/nested-object.json
```
