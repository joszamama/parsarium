# aws-smithy-json — JSON / Rust

**Verified path in a bounded pilot cell.** This release was run on two small valid RFC 8259 JSON controls; the cell search remains open.

- **Pinned release:** `0.65.1`; [source crate](https://static.crates.io/crates/aws-smithy-json/aws-smithy-json-0.65.1.crate), SHA-256 `b45f9fc77ffe92c92c341165a01a565bd30c39ecf5aa8c0719b41719009604f9`.
- **License:** Apache-2.0; the release license file is hashed in [source-lock.json](../../../../projects/json/rust/aws_smithy_json/source-lock.json).
- **Parser family:** AWS Smithy JSON's own token-stream parser in `src/deserialize.rs`. The package is used by generated AWS SDK clients, but the pinned source documents a public generic byte-input iterator. Its `TESTING.md` includes a local-file JSONTestSuite runner.
- **Local input API:** [`aws_smithy_json::deserialize::json_token_iter(&[u8])`](https://docs.rs/crate/aws-smithy-json/0.65.1/source/src/deserialize.rs), yielding structural and scalar tokens. The adapter decodes escaped strings and requires one balanced root value.
- **Adoption proxy:** 59,322,077 crates.io recent downloads (90 days) in the [snapshot](../../../../data/rust/json/registry-snapshot.json), ranked only against verified Rust JSON paths. This includes transitive AWS SDK pulls.
- **Valid controls:** [`nested-object.json`](../../../../controls/json/nested-object.json) and [`nested-array.json`](../../../../controls/json/nested-array.json).
- **Evidence:** [catalog record](../../../../data/rust/json/parsers.json), [base receipt](../../../../projects/json/rust/aws_smithy_json/verification.json), [AFL++ overlay](../../../../fuzzing/afl-native/json/rust/aws_smithy_json/verification.json).

## Observed structure

The adapter reports root type, object and array counts, boolean and null counts, nesting depth, decoded value strings and numbers, and top-level keys. The first control produced:

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

The second control has an array root and a different structure; its exact expected output is pinned in the [manifest](../../../../projects/json/rust/aws_smithy_json/manifest.json).

The source iterator permits multiple values and documents permissive number syntax. The adapter requires one balanced root, and these receipts establish only the two valid controls. No malformed-input behavior was tested.

## Run this target

```sh
python3 parsarium.py build json rust aws_smithy_json
python3 parsarium.py run json rust aws_smithy_json controls/json/nested-object.json
python3 parsarium.py afl build json rust aws_smithy_json
python3 parsarium.py afl prepare json rust aws_smithy_json runs/json-aws_smithy_json-afl
```

`afl prepare` seeds a run without starting a mutation campaign. The verification gate checks only the two valid controls, repeated AFL++ feedback, and AWS Smithy JSON parser source coverage.
