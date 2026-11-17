# jsonparse — JSON / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.3.1`
- **License:** MIT
- **Parser family:** jsonparse byte-level tokenizer and stack value builder
- **Local input API:** `new Parser(); parser.onValue = root callback when this.stack is empty; parser.write(local Buffer)`
- **Documentation:** [API reference](<https://github.com/creationix/jsonparse/blob/1480064a3040cec3f27aa929dd1d1469150b8737/examples/twitterfeed.js>) · [API reference](<https://github.com/creationix/jsonparse/blob/1480064a3040cec3f27aa929dd1d1469150b8737/test/primitives.js>)
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

The 1.3.1 README documents no API; it says only that this is a streaming JSON parser. The API is the one shown by the packaged example (new Parser(), onValue with an empty-stack root, write(chunk)) and tests. The tarball gitHead is 1480064a3040cec3f27aa929dd1d1469150b8737; jsonparse.js in the tarball is byte-identical to that commit. jsonparse has no end() call and accepts a stream of concatenated values, so the adapter, not the package, rejects a second root, an open container, or an unfinished token. From source reading (not run): a number token accepts any run of digits . e E + - and is checked only by Number(), so leading zeros are not rejected; an integer digit string that does not round-trip through Number is emitted as a string; a bare number root is emitted only when a following byte ends the token. Only the two valid controls were run. Both valid controls, nested-object.json and nested-array.json, produce the exact pinned summaries; the adapter returns a summary only after one complete root object or array has been delivered.

## Run this target

```sh
python3 parsarium.py build json javascript jsonparse
python3 parsarium.py run json javascript jsonparse controls/json/nested-object.json
```
