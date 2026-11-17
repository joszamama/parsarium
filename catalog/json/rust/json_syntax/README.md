# json-syntax — JSON / Rust

**Verified path in a bounded pilot cell.** Release 0.13.1 was run on two small valid RFC 8259 JSON controls. The cell search remains open.

- **Source:** [json-syntax 0.13.1 crate](https://static.crates.io/crates/json-syntax/json-syntax-0.13.1.crate), SHA-256 `1a77d52c04b5ef283ff6843702206599110495080b0d26aef81a3f0bbca30b16`.
- **License:** MIT OR Apache-2.0; both release license files are pinned in [source-lock.json](../../../../projects/json/rust/json_syntax/source-lock.json).
- **Local input API:** [`JsonValue::parse_slice(&[u8])`](https://docs.rs/json-syntax/0.13.1/json_syntax/parse/trait.JsonParse.html) parses a complete local JSON byte slice into its own tree and code map.
- **Parser family:** json-syntax strict parser and code map in `src/parse`; `json-number` stores numeric lexical form. The optional serde_json feature is disabled.
- **Adoption:** 702,428 crates.io recent downloads (90 days) in the [snapshot](../../../../data/rust/json/registry-snapshot.json), compared only with Rust JSON paths. Downloads can include transitive pulls.
- **Controls:** [nested object](../../../../controls/json/nested-object.json) and [nested array](../../../../controls/json/nested-array.json).
- **Evidence:** [catalog record](../../../../data/rust/json/parsers.json), [base receipt](../../../../projects/json/rust/json_syntax/verification.json), [AFL++ receipt](../../../../fuzzing/afl-native/json/rust/json_syntax/verification.json).

## Observed result

The first control yielded an object root, five objects, three arrays, four container levels, decoded text including `café "quoted"`, and seven sorted top-level keys. The second yielded an array root with a different structure. Both exact summaries are pinned in the [manifest](../../../../projects/json/rust/json_syntax/manifest.json).

The harness traverses the crate's own parsed tree. `serde_json` encodes the summary only and never parses input. The two controls verify this path's format-aware behavior; other JSON cases remain untested.

## Run

```sh
python3 parsarium.py build json rust json_syntax
python3 parsarium.py run json rust json_syntax controls/json/nested-object.json
python3 parsarium.py afl build json rust json_syntax
python3 parsarium.py afl prepare json rust json_syntax runs/json-json-syntax-afl
```

`afl prepare` seeds a run without starting a campaign. The verification gate checks both valid controls, parser source coverage, and exact repeated input-dependent AFL++ feedback.
