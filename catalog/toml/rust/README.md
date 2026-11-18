# TOML / Rust — pilot

**Status:** pilot_nine_selected_search_bounded; incomplete. 9 verified third-party paths, 0 verified standard APIs, 9 verified Docker harnesses.

Bounded TOML search captured 2026-11-17: 3 crates.io queries, 300 recorded hits (283 unique), at most 100 per query; round 4 (2026-11-18) added download-sorted and keyword/category crates.io listings and the toml-lang wiki lists (registry-snapshot round_4_targeted_lookups). Nine paths are verified. toml 1.2.1+spec-1.1.0 and toml_edit 0.25.19+spec-1.1.0 both lex and parse through the same toml_parser 1.1.5 crate and build their own trees from its events, so they are one parser family with two tree builders; their coverage is recorded separately for the own crate and for toml_parser. taplo 0.14.0, boml 2.0.1, toml-spanner 1.0.3, tomlproc 0.1.2, soml 0.2.0, toml_dom 0.6.0 and kabosu 0.2.1 are independent parser families. Every selected overlay instruments only the path's own crate (plus toml_parser for toml and toml_edit) and fixes getrandom with an AFL_PRELOAD shim; taplo also installs a fixed ahash seed source. Ten afl-showmap repeats per control are identical for every path. The four round-4 paths rank on small recent-download counts (700, 112, 85 and 46), which are weak adoption evidence; round-4 values come from the same crates.io search API on 2026-11-18, one day after the recorded snapshot. Not selected: basic-toml 0.1.10 and toml-span 0.7.2 (no datetime type; both controls rejected), nanoserde 0.2.1 (rejects hexadecimal integers; one f64 number type), deser-toml 0.10.2 (no documented generic value view), antlr-rust-toml-parser 0.34.0 (7,967; demoted at integrator review: it returns flat assignments and table headers, so nesting tables and dotted keys would be harness interpretation under the concrete-syntax-tree rule), facet-toml 0.46.1 (toml_parser family; date-times reach facet as strings), fig-toml 7.0.0, tomlsmith 0.4.1, babbel_toml 0.3.0 and oak-toml 0.0.11 (date-times kept only as source text, so the offset instant would need harness-side text parsing), olpat (a taplo fork) and flyleaf-core (over toml_edit). Fig-toml (1,397), oak-toml (990), tomlsmith (493) and babbel_toml (133) have higher counts than the four round-4 paths but are unverified leads, so ranks cover verified paths only. The pinned releases implement TOML 1.0 or 1.1; two valid TOML 1.0.0 controls establish only the tested subset; malformed input, huge documents and TOML 1.1 features are untested. Recent downloads include transitive dependency pulls (Cargo itself depends on toml and toml_edit). The cell stays at nine below the ceiling; own-parser crates below 46 recent downloads in the round-4 listings (toml_document, tomling, tomboy-toml-dom, toml-shelby, tommy, brittle, neco-toml, kosmetic-syntax) were not run. Round 6 (2026-11-18) tried the toml-test-matrix parser list, crates.io reverse dependencies of the toml-test tooling crates and 39 further name lookups. tomling 0.3.0 (30) rejects both controls (escaped quotes in basic strings), tomllib 0.1.2 (99) keeps integers, floats and strings as source text and cannot represent a local time, toml-parse (172) is a rowan syntax tree only, toml_reader wraps toml, env_toml is a toml fork and picotoml has no value type. The cell stays at nine.

[Ranking and search limits](../../../data/rust/toml/ranking.md) · [Standard API inventory](../../../data/rust/toml/standard.json)

## Third-party parsers

- [toml](toml/README.md) — verified Docker harness
- [toml_edit](toml-edit/README.md) — verified Docker harness
- [taplo](taplo/README.md) — verified Docker harness
- [boml](boml/README.md) — verified Docker harness
- [toml-spanner](toml-spanner/README.md) — verified Docker harness
- [tomlproc](tomlproc/README.md) — verified Docker harness
- [soml](soml/README.md) — verified Docker harness
- [toml_dom](toml-dom/README.md) — verified Docker harness
- [kabosu](kabosu/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
