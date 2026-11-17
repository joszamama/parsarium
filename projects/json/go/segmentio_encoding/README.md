# github.com/segmentio/encoding/json — JSON / Go

Pinned release: `v0.5.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Scoped catalog row: API, control result, adoption metric, and parser family](../../../../data/go/json/segmentio_encoding-parser.json)

## Run from the repository root

```sh
python3 parsarium.py build json go segmentio_encoding
python3 parsarium.py run json go segmentio_encoding controls/json/nested-object.json
python3 parsarium.py replay json go segmentio_encoding CORPUS_DIR runs/json-segmentio_encoding-replay
python3 parsarium.py afl build json go segmentio_encoding
python3 parsarium.py afl prepare json go segmentio_encoding runs/json-segmentio_encoding-afl
python3 projects/json/go/segmentio_encoding/verify-feedback.py
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

## Parser path

The harness calls the documented `json.Unmarshal([]byte, any)` with a `*any` target. `Unmarshal` calls the package's own `Parse(b, x, 0)`, and decoding into `any` goes through `decoder.decodeInterface`, which tokenizes with `parseValue` in `parse.go` and builds maps and slices in `decode.go`. The package imports the standard `encoding/json` only for shared types and for `Compact`, `HTMLEscape` and `Indent`, which the harness does not call.

## Verification

- Module zip `v0.5.4` sha256 `2189639875fe1153571445dc9b5dcaf221554143fe6701426fba69aa77780681` (Go proxy origin commit `7d5a25dbc5da13aed3cb047a127e4d0e96f536fb`), dependency `github.com/segmentio/asm v1.1.3` sha256 `1911909b67b0f86c04fb895434c4072602d7b7523350ab45cb1549425b3a3b1b`. Both are checked in the Dockerfile. License: MIT.
- Both valid controls (`nested-object.json`, `nested-array.json`) match exact structural summaries. `verify-feedback.py` recomputes both summaries with Python's `json` module and checks them against the harness constants and the manifest.
- The object control covers 367 lines in 5 files of the pinned `json` package: `parse.go` 217, `decode.go` 106, `codec.go` 23, `json.go` 17, `int.go` 4.
- AFL++ feedback is scoped to the `json` package: 273 parser features and 293 tuples on the object control. Repeats of each control are identical, and the array control changes 14 parser features and 14 tuples ([receipt](../../../../fuzzing/afl-native/json/go/segmentio_encoding/differential.json)).

## Adoption

pkg.go.dev shows 348 importing packages. That matches the 2026-11-17 registry snapshot and my recheck at 2026-11-17T14:34Z. Among the selected Go JSON paths it ranks below fastjson (895), so it would be eighth of eight.
