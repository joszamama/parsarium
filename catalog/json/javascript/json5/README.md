# json5 — JSON / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.2.3`
- **License:** MIT
- **Parser family:** json5 character lexer and parse-state machine
- **Local input API:** `JSON5.parse(text) on local bytes decoded as strict UTF-8 text; summary and type-tagged tree walk the returned value`
- **Documentation:** [API reference](<https://github.com/json5/json5/blob/c3a75242772a5026a49c4017a16d9b3543b62776/README.md#json5parse>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/javascript/json/parsers.json) · [control result](../../../../data/javascript/json/verification.json)

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

## Verification scope

The README documents JSON5.parse(text[, reviver]) as parsing a JSON5 string and states that JSON5 is a superset of JSON (valid JSON files are valid JSON5); text input qualifies because the adapter reads the bytes locally and json5 parses their structure. README.md and lib/{index,parse,util,unicode}.js at gitHead c3a75242772a5026a49c4017a16d9b3543b62776 (tag v2.2.3) are byte-identical to the tarball. Local bytes are decoded with TextDecoder('utf-8', {fatal: true, ignoreBOM: true}); JSON5.parse is called once without a reviver, and there is no JSON.parse fallback. The adapter turns the returned value into a type-tagged tree (numbers as IEEE 754 double bits, object members in Object.keys order) and derives the summary from that tree. On both valid controls, nested-object.json and nested-array.json, the tree equals one produced by an independent Python json oracle over the same bytes and the summary equals the pinned summary (data/javascript/json/json5-tree-verification.json). From source reading, not run: the default lex state skips JSON5 whitespace (U+00A0, U+FEFF, U+2028/9, Unicode Space_Separator, \v, \f) and comments; the value states accept single-quoted strings, unquoted identifier keys, hexadecimal, Infinity, NaN, leading '+' and leading or trailing decimal points; trailing commas are accepted; unescaped control characters other than CR and LF are kept inside strings; unescaped U+2028/2029 in strings print a console.warn. So invalid RFC 8259 input can be accepted. Duplicate keys keep the last value, members are set with Object.defineProperty so a __proto__ key becomes an own property, and integer-like keys follow JavaScript property order in Object.keys; the controls have none of these. Only the two valid controls were run.

## Run this target

```sh
python3 parsarium.py build json javascript json5
python3 parsarium.py run json javascript json5 controls/json/nested-object.json
```
