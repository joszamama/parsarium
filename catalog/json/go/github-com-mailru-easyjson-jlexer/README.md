# github.com/mailru/easyjson/jlexer — JSON / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v0.9.2`
- **Upstream:** [source repository](<https://github.com/mailru/easyjson>) · [pkg.go.dev](<https://pkg.go.dev/github.com/mailru/easyjson/jlexer>)
- **License:** MIT
- **Parser family:** easyjson jlexer own Go tokenizer
- **Local input API:** `jlexer.Lexer{Data: []byte}.Interface() over one complete local JSON byte slice, then Lexer.Consumed() and Lexer.Error()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/mailru/easyjson@v0.9.2/jlexer#Lexer.Interface>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/go/json/parsers.json) · [control result](../../../../data/go/json/verification.json)

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

Both valid controls (nested-object.json and nested-array.json) match exact structural summaries recomputed with Python's json module as an independent oracle. The object control covers 212 lines in the pinned jlexer package (lexer.go 211, bytestostr.go 1). AFL++ feedback is scoped to the jlexer package: 126 parser features and 146 tuples on the object control; repeats of each control are identical, and the array control changes 6 parser features and 6 tuples. The easyjson v0.9.2 module zip and the josharian/intern v1.0.0 dependency zip are sha256-checked in the Dockerfile. pkg.go.dev Imported by 3,424 comes from the same 2026-11-17 snapshot as the other Go JSON rows and was rechecked at 2026-11-17T15:03Z.

## Run this target

```sh
python3 parsarium.py build json go github_com_mailru_easyjson_jlexer
python3 parsarium.py run json go github_com_mailru_easyjson_jlexer controls/json/nested-object.json
```
