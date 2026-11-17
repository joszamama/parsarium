# sonic-rs — JSON / Rust

**Verified path in a bounded pilot cell.** This release was run on two small valid RFC 8259 JSON controls; the cell search remains open.

- **Pinned release:** `0.5.11`; [source crate](https://static.crates.io/crates/sonic-rs/sonic-rs-0.5.11.crate), SHA-256 `a1cd78ade69b3f8bb19338beb2f436f7fa85b9bd6330eb0962a1f4b8491515fc`.
- **License:** Apache-2.0; the release's license file is hashed in [source-lock.json](../../../../projects/json/rust/sonic_rs/source-lock.json). Its source includes notices for referenced upstream work.
- **Parser family:** sonic-rs SIMD parser with its own `src/parser.rs` and arena-backed `Value` DOM; it depends on `sonic-simd` and `sonic-number`. The project acknowledges ideas and code from simdjson, serde_json and others; it does not route the input through the selected `serde_json` or `simd-json` crates. `serde_json` in this adapter encodes the summary only.
- **Local input API:** [`sonic_rs::from_slice::<sonic_rs::Value>(&[u8])`](https://docs.rs/sonic-rs/0.5.11/sonic_rs/fn.from_slice.html).
- **Adoption proxy:** 3,669,348 crates.io recent downloads (90 days) in the [snapshot](../../../../data/rust/json/registry-snapshot.json), ranked only against other verified Rust JSON paths.
- **Platform:** pinned linux/arm64 Docker build. AArch64 SIMD support is documented. The portable container omits `-C target-cpu=native`, which sonic-rs recommends for maximum speed; no performance claim or identical coverage map is made for other CPUs.
- **Valid controls:** [`nested-object.json`](../../../../controls/json/nested-object.json) and [`nested-array.json`](../../../../controls/json/nested-array.json).
- **Evidence:** [catalog record](../../../../data/rust/json/parsers.json), [base receipt](../../../../projects/json/rust/sonic_rs/verification.json), [AFL++ overlay](../../../../fuzzing/afl-native/json/rust/sonic_rs/verification.json).

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

The second control has an array root and a different structure; its exact expected output is pinned in the [manifest](../../../../projects/json/rust/sonic_rs/manifest.json).

## Run this target

```sh
python3 parsarium.py build json rust sonic_rs
python3 parsarium.py run json rust sonic_rs controls/json/nested-object.json
python3 parsarium.py afl build json rust sonic_rs
python3 parsarium.py afl prepare json rust sonic_rs runs/json-sonic_rs-afl
```

`afl prepare` seeds a run without starting a mutation campaign. The verification gate checks only the two valid controls, repeated AFL++ feedback, and sonic-rs parser source coverage.
