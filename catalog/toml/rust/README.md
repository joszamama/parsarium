# TOML / Rust — pilot

**Status:** pilot_two_selected_search_bounded; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Bounded TOML search captured 2026-11-17: 3 crates.io queries, 300 recorded hits (283 unique), at most 100 per query. Two paths are verified: toml 1.2.1+spec-1.1.0 and toml_edit 0.25.19+spec-1.1.0. Both lex and parse through the same toml_parser 1.1.5 crate and build their own trees from its events, so they are one parser family with two tree builders, not two independent parsers; their coverage is recorded separately for the own crate and for toml_parser. basic-toml 0.1.10 and toml-span 0.7.2 have no datetime type and reject both controls at the first offset date-time, so they stay leads. 7 leads remain, five of them not run (toml_parser has no value tree). The pinned releases implement TOML 1.1.0; two valid TOML 1.0.0 controls establish only the tested subset; malformed input, huge documents and TOML 1.1 features are untested. Recent downloads include transitive dependency pulls (Cargo itself depends on toml and toml_edit). toml_edit stores tables in IndexMaps with std RandomState hashing; without the overlay's getrandom AFL_PRELOAD shim, 1 of 5 afl-showmap runs on service-config.toml gave 1,546 instead of 1,530 tuples (checked 2026-11-17), so its overlay fixes the hash keys (afl_fixed_hashmap_keys) and then repeats are identical.

[Ranking and search limits](../../../data/rust/toml/ranking.md) · [Standard API inventory](../../../data/rust/toml/standard.json)

## Third-party parsers

- [toml](toml/README.md) — verified Docker harness
- [toml_edit](toml-edit/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
