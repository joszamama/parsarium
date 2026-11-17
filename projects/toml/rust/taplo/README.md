# taplo — TOML / Rust

Pinned release: `0.14.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/rust/taplo/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml rust taplo
python3 parsarium.py run toml rust taplo controls/toml/service-config.toml
python3 parsarium.py replay toml rust taplo CORPUS_DIR runs/toml-taplo-replay
python3 parsarium.py afl build toml rust taplo
python3 parsarium.py afl prepare toml rust taplo runs/toml-taplo-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** taplo 0.14.0 lexes with a logos-derived token enum and parses into a rowan green tree; Parse::into_dom() then merges header and dotted keys into DOM tables and decodes scalars lazily (IntegerValue, f64, unescaped strings, and DateTimeValue built with the time crate). Only the taplo crate is instrumented for AFL++; logos, rowan, time and ahash are uninstrumented. DOM table lookups use ahash, so the AFL++ overlay fixes getrandom bytes.
