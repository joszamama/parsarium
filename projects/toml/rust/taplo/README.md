# taplo — TOML / Rust

Pinned release: `0.14.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/rust/taplo/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml rust taplo
python3 parsarium.py run toml rust taplo controls/toml/service-config.toml
python3 parsarium.py replay toml rust taplo CORPUS_DIR runs/toml-taplo-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build toml rust taplo
python3 parsarium.py afl prepare toml rust taplo runs/toml-taplo-afl --fandango 100
python3 parsarium.py afl run runs/toml-taplo-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** taplo 0.14.0 lexes with a logos-derived token enum and parses into a rowan green tree; Parse::into_dom() then merges header and dotted keys into DOM tables and decodes scalars lazily (IntegerValue, f64, unescaped strings, and DateTimeValue built with the time crate). Only the taplo crate is instrumented for AFL++; logos, rowan, time and ahash are uninstrumented. DOM table lookups use ahash, so the AFL++ overlay fixes getrandom bytes.
