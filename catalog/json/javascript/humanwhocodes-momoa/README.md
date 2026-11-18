# @humanwhocodes/momoa — JSON / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `3.3.13`
- **Upstream:** [source repository](<https://github.com/humanwhocodes/momoa>) · [npm](<https://www.npmjs.com/package/@humanwhocodes/momoa>)
- **License:** Apache-2.0
- **Parser family:** momoa tokenizer and recursive-descent AST parser
- **Local input API:** `parse(text, {mode: 'json'}) on local bytes decoded as strict UTF-8 text; summary walks the returned Document AST`
- **Documentation:** [API reference](<https://github.com/humanwhocodes/momoa/blob/625bcbec28623ccebb1da837c71389cf38014800/js/README.md#parsing>)
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

momoa's README documents parse(text) on a JSON string with mode "json" as the default; text input qualifies because the adapter reads it locally and momoa parses its structure. Local bytes are decoded with TextDecoder('utf-8', {fatal: true, ignoreBOM: true}), so invalid UTF-8 is rejected before the parser and a BOM is passed through to momoa. parse() throws on any token after the first value. The adapter summarizes the AST nodes directly (Object.members, Array.elements, String/Number/Boolean/Null values) and does not call evaluate() or JSON.parse. The AST keeps every member, so top_level_keys would list duplicate keys more than once; the controls have none. js/README.md at gitHead 625bcbec28623ccebb1da837c71389cf38014800 (tag momoa-js-v3.3.13) is byte-identical to the tarball README. Both valid controls, nested-object.json and nested-array.json, produce the exact pinned summaries, which an independent Python json summary of the same control bytes also reproduces (tests/test_javascript_json_momoa.py). Only the two valid controls were run.

## Run this target

```sh
python3 parsarium.py build json javascript humanwhocodes_momoa
python3 parsarium.py run json javascript humanwhocodes_momoa controls/json/nested-object.json
```
