# miniserde — JSON / Rust

**Verified path in a bounded pilot cell.** Release 0.1.46 was run on two small valid RFC 8259 JSON controls. The cell search remains open.

- **Source:** [miniserde 0.1.46 crate](https://static.crates.io/crates/miniserde/miniserde-0.1.46.crate), SHA-256 `e8f82621301d3b99a1542736de96e5df69865b235987d6470b28c7aa670cfeb1`.
- **License:** MIT OR Apache-2.0; both release license files are hashed in [source-lock.json](../../../../projects/json/rust/miniserde/source-lock.json).
- **Local input API:** [`miniserde::json::from_str::<Value>(&str)`](https://docs.rs/miniserde/0.1.46/miniserde/json/fn.from_str.html) parses local UTF-8 JSON text into the crate's generic `Value` tree.
- **Parser family:** miniserde's own non-recursive deserializer in `src/json/de.rs`, separate from serde_json's parser despite their common author. `serde_json` in this harness only encodes the summary.
- **Adoption:** 1,335,406 crates.io recent downloads (90 days) in the [snapshot](../../../../data/rust/json/registry-snapshot.json), compared only with Rust JSON paths. Downloads can include transitive pulls.
- **Controls:** [nested object](../../../../controls/json/nested-object.json) and [nested array](../../../../controls/json/nested-array.json).
- **Evidence:** [catalog record](../../../../data/rust/json/parsers.json), [base receipt](../../../../projects/json/rust/miniserde/verification.json), [AFL++ receipt](../../../../fuzzing/afl-native/json/rust/miniserde/verification.json).

## Observed result

The first control yielded an object root, five objects, three arrays, four container levels, decoded text including `café "quoted"`, and seven sorted top-level keys. The second yielded an array root with a different structure. Both exact summaries are pinned in the [manifest](../../../../projects/json/rust/miniserde/manifest.json).

The adapter walks miniserde's `Value` tree iteratively and reports numbers as `f64` for the common control summary. These receipts establish only the two valid controls.

## Run

```sh
python3 parsarium.py build json rust miniserde
python3 parsarium.py run json rust miniserde controls/json/nested-object.json
python3 parsarium.py afl build json rust miniserde
python3 parsarium.py afl prepare json rust miniserde runs/json-miniserde-afl
```

`afl prepare` seeds a run without starting a campaign. The verification gate checks both valid controls, miniserde source coverage, and exact repeated input-dependent AFL++ feedback.
