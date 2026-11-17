# hifijson — JSON / Rust

**Verified path in a bounded pilot cell.** Release 0.5.0 was run on two small valid RFC 8259 JSON controls. The cell search remains open.

- **Source:** [hifijson 0.5.0 crate](https://static.crates.io/crates/hifijson/hifijson-0.5.0.crate), SHA-256 `242402749acf71e6f32f5857598b7002c4058a4e3c3b22b4c7d51cab9aea754e`.
- **License:** MIT is declared in the pinned release Cargo.toml. No LICENSE file is bundled in that crate; its manifest hash and source commit are recorded in [source-lock.json](../../../../projects/json/rust/hifijson/source-lock.json).
- **Local input API:** [`SliceLexer::new(&[u8])`](https://docs.rs/hifijson/0.5.0/hifijson/struct.SliceLexer.html), followed by `Lex::exactly_one` and `value::parse_bounded`, produces hifijson's own `Value` tree.
- **Parser family:** hifijson's independent lexer and recursive value parser. `serde_json` only encodes the observed summary.
- **Adoption:** 2,630,468 crates.io recent downloads (90 days) in the [snapshot](../../../../data/rust/json/registry-snapshot.json), compared only with Rust JSON paths. Downloads can include transitive pulls.
- **Controls:** [nested object](../../../../controls/json/nested-object.json) and [nested array](../../../../controls/json/nested-array.json).
- **Evidence:** [catalog record](../../../../data/rust/json/parsers.json), [base receipt](../../../../projects/json/rust/hifijson/verification.json), [AFL++ receipt](../../../../fuzzing/afl-native/json/rust/hifijson/verification.json).

## Observed result

The first control yielded an object root, five objects, three arrays, four container levels, decoded text including `café "quoted"`, and seven sorted top-level keys. The second yielded an array root with a different structure. Both exact summaries are pinned in the [manifest](../../../../projects/json/rust/hifijson/manifest.json).

hifijson preserves source number spelling in its own value representation. The harness converts numbers to `f64` only for the common control summary. The crate's default parser permits concatenated JSON roots; the adapter requires exactly one root and bounds recursion at 256 levels. These receipts establish only the two valid controls.

## Run

```sh
python3 parsarium.py build json rust hifijson
python3 parsarium.py run json rust hifijson controls/json/nested-object.json
python3 parsarium.py afl build json rust hifijson
python3 parsarium.py afl prepare json rust hifijson runs/json-hifijson-afl
```

`afl prepare` seeds a run without starting a campaign. The verification gate checks both valid controls, hifijson source coverage, and repeated input-dependent AFL++ feedback.
