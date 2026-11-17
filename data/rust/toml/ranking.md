# RUST × TOML: selected parsers

2 control-verified third-party paths; bounded pilot scope. Both share the toml_parser lexer and event parser. TOML parser leads that are not verified are listed in [leads.json](leads.json).

## Primary within-cell adoption metric

crates.io recent downloads (90 days), from the search API in [registry-snapshot.json](registry-snapshot.json), captured 2026-11-17.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [toml](https://docs.rs/toml/1.2.1+spec-1.1.0/toml/fn.from_str.html) | 1.2.1+spec-1.1.0 | 323,348,893 | `from_str::<toml::Table>(&str)` over locally decoded UTF-8 text: Table/Value tree with typed scalars and `toml_datetime` date, time and offset parts | toml_parser 1.1.5 lexer and event parser (shared with toml_edit); toml's own DeTable/DeValue and Table/Value builder |
| 2 | [toml_edit](https://docs.rs/toml_edit/0.25.19+spec-1.1.0/toml_edit/struct.DocumentMut.html) | 0.25.19+spec-1.1.0 | 292,512,904 | `str::parse::<DocumentMut>()` over locally decoded UTF-8 text: format-preserving Item/Value tree; decoded values observed through `Formatted::value()` | toml_parser 1.1.5 lexer and event parser (shared with toml); toml_edit's own format-preserving Document/Item/Value builder |

Unverified TOML parser leads, by the same metric: toml_parser 197,554,106 (lexer and event parser without a value tree; covered as the underlying parser of both selected paths), basic-toml 20,713,123 (control failed: release 0.1.10 has no datetime type and rejects both controls at the first offset date-time with "invalid number at line 8 column 9" and "invalid number at line 27 column 10"), toml-span 6,719,423 (control failed: release 0.7.2 has no datetime variant and rejects both controls with `InvalidNumber` at the first offset date-time), taplo 703,745, nanoserde 488,505, boml 136,881 and toml-spanner 44,429 (not run). See [leads.json](leads.json). Recent downloads include transitive dependency pulls; Cargo itself depends on toml and toml_edit, and the two counts overlap.

## Standard library

None documented in the Rust 1.99.1 standard library; see [standard.json](standard.json).

Ranks compare only verified paths. toml and toml_edit are one parser family: neither has its own lexer, and each builds its own tree from toml_parser events. Their receipts record line coverage separately for the own crate and for toml_parser, and their AFL++ overlays instrument only those two crates.
