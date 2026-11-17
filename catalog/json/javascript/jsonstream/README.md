# JSONStream — JSON / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.3.5`
- **License:** (MIT OR Apache-2.0)
- **Parser family:** jsonparse byte-level tokenizer and stack value builder (via JSONStream path filter)
- **Local input API:** `stream = JSONStream.parse([]); stream.on('data'|'error'|'end'); stream.end(local Buffer)`
- **Documentation:** [API reference](<https://github.com/dominictarr/JSONStream/blob/0593d4b4e6c63c6c0e2e68463538fd83bd1eb964/readme.markdown>) · [API reference](<https://github.com/dominictarr/JSONStream/blob/0593d4b4e6c63c6c0e2e68463538fd83bd1eb964/test/test2.js>)
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

JSONStream 1.3.5 is a distinct npm package and API path, not an independent parser engine. Its index.js (no JSON.parse call) wraps one jsonparse 1.3.1 Parser in a through 2.3.8 stream: write() hands each Buffer to Parser.write, its onValue override filters values by path, and its onToken override queues each completed root when the path is empty. Tokenizing, UTF-8 and \u escape handling, number conversion and value building are jsonparse's, so it shares the jsonparse parser family (verified separately as its own path). The README says an empty or null path emits no 'data' events; the code and the packaged test/test2.js (JSONStream.parse([]) emits the whole root once) show otherwise, and the adapter follows the test. The tarball gitHead is 0593d4b4e6c63c6c0e2e68463538fd83bd1eb964; index.js and test/test2.js are byte-identical to that commit. JSONStream has no end-of-input completeness check and accepts concatenated roots, and its parser object is private, so the adapter can only require exactly one emitted root, no 'error' and an 'end' event: an unfinished token or open container after one complete root is not detected through this API. From source reading (not run): a root that is falsy (0, false, null, "") is never emitted, because onToken queues stream.root only when it is truthy; jsonparse's number and big-integer behaviour applies unchanged. Only the two valid controls were run. Both valid controls, nested-object.json and nested-array.json, produce the exact pinned summaries.

## Run this target

```sh
python3 parsarium.py build json javascript jsonstream
python3 parsarium.py run json javascript jsonstream controls/json/nested-object.json
```
