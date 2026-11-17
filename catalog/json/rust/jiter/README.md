# jiter — JSON / Rust

**Verified path in a bounded pilot cell.** This release was run on two small valid RFC 8259 JSON controls; the cell search remains open.

- **Pinned release:** `0.19.0`; [source crate](https://static.crates.io/crates/jiter/jiter-0.19.0.crate), SHA-256 `4027f86130c7a1997f880ed407580e58514b867af49e7ce44370f80fa6ff999f`.
- **License:** MIT; the release license file is hashed in [source-lock.json](../../../../projects/json/rust/jiter/source-lock.json).
- **Parser family:** Jiter’s own Rust JSON tokenizer and value builder. The separate Python `pydantic` path uses pydantic-core 2.50.4 with Jiter 0.18.0; this Rust path pins Jiter 0.19.0. They share a parser family across ecosystems, and their adoption numbers are never compared across ecosystems.
- **Local input API:** [`jiter::JsonValue::parse(&[u8], false)`](https://docs.rs/jiter/0.19.0/jiter/enum.JsonValue.html#method.parse), with `allow_inf_nan=false` for strict JSON. This builds an untyped value tree from local bytes.
- **Adoption proxy:** 5,274,664 crates.io recent downloads (90 days) in the [snapshot](../../../../data/rust/json/registry-snapshot.json), ranked only against other verified Rust JSON paths.
- **Valid controls:** [`nested-object.json`](../../../../controls/json/nested-object.json) and [`nested-array.json`](../../../../controls/json/nested-array.json).
- **Evidence:** [catalog record](../../../../data/rust/json/parsers.json), [base receipt](../../../../projects/json/rust/jiter/verification.json), [AFL++ overlay](../../../../fuzzing/afl-native/json/rust/jiter/verification.json).

## Observed structure

The adapter reports root type, object and array counts, boolean and null counts, nesting depth, decoded strings and numbers, and top-level keys. The first control produced:

```json
{
  "arrays": 3,
  "booleans": 2,
  "max_depth": 4,
  "nulls": 1,
  "numbers": [
    -2.5,
    1.0,
    1.0,
    2.0,
    2.0
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

The second control has an array root and a different structure; its exact expected output is pinned in the [manifest](../../../../projects/json/rust/jiter/manifest.json).

## Run this target

```sh
python3 parsarium.py build json rust jiter
python3 parsarium.py run json rust jiter controls/json/nested-object.json
python3 parsarium.py afl build json rust jiter
python3 parsarium.py afl prepare json rust jiter runs/json-jiter-afl
```

`afl prepare` seeds a run without starting a mutation campaign. The verification gate checks only the two valid controls, repeated AFL++ feedback, and Jiter parser source coverage.
