# gjson — JSON / Rust

**Verified path in a bounded pilot cell.** Release 0.8.1 was run on two small valid RFC 8259 JSON controls. The cell search remains open.

- **Source:** [gjson 0.8.1 crate](https://static.crates.io/crates/gjson/gjson-0.8.1.crate), SHA-256 `43503cc176394dd30a6525f5f36e838339b8b5619be33ed9a7783841580a97b6`.
- **License:** MIT; the release license file hash is pinned in [source-lock.json](../../../../projects/json/rust/gjson/source-lock.json).
- **Local input API:** [`gjson::valid(&str)`](https://docs.rs/gjson/0.8.1/gjson/fn.valid.html) checks the complete local JSON text, then [`gjson::parse(&str)`](https://docs.rs/gjson/0.8.1/gjson/fn.parse.html) and `Value::each` lazily scan every child.
- **Parser family:** tidwall GJSON path-query design, shared with the selected [Go gjson](../../../../data/go/json/parsers.json) path. This pinned Rust crate owns its separate scanner and validator implementation.
- **Adoption:** 1,151,387 crates.io recent downloads (90 days) in the [snapshot](../../../../data/rust/json/registry-snapshot.json), compared only with Rust JSON paths. Downloads can include transitive pulls.
- **Controls:** [nested object](../../../../controls/json/nested-object.json) and [nested array](../../../../controls/json/nested-array.json).
- **Evidence:** [catalog record](../../../../data/rust/json/parsers.json), [base receipt](../../../../projects/json/rust/gjson/verification.json), [AFL++ receipt](../../../../fuzzing/afl-native/json/rust/gjson/verification.json).

## Observed result

The first control yielded an object root, five objects, three arrays, four container levels, decoded text including `café "quoted"`, and seven sorted top-level keys. The second yielded an array root with a different structure. Both exact summaries are pinned in the [manifest](../../../../projects/json/rust/gjson/manifest.json).

`parse` and `get` alone assume valid input and serve path queries. The harness calls the crate's whole-root `valid` first, then traverses every nested object and array through `Value::each`. This is evidence of a format-aware, validating scan on the two controls; it is not a claim that `parse` alone validates arbitrary JSON. The adapter bounds traversal at 256 levels.

## Run

```sh
python3 parsarium.py build json rust gjson
python3 parsarium.py run json rust gjson controls/json/nested-object.json
python3 parsarium.py afl build json rust gjson
python3 parsarium.py afl prepare json rust gjson runs/json-gjson-afl
```

`afl prepare` seeds a run without starting a campaign. The verification gate checks both valid controls, gjson source coverage, and exact repeated input-dependent AFL++ feedback.
