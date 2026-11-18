# TOML / C — pilot

**Status:** pilot_search_bounded_none_selected; incomplete. 0 verified third-party paths, 0 verified standard APIs, 0 verified Docker harnesses.

Bounded TOML search captured 2026-11-17: 3 queries, 100 recorded hits (86 unique), at most 100 per query. No C TOML library appears in Debian popcon or Conan Center, so no C path has the primary metric or a Debian fallback of at least 1,000, and none is selected. tomlc17 R261116 and toml-c (tomlc99 fork, commit 6a38d404) passed both valid controls with exact typed trees, parser coverage and stable AFL++ feedback; they stay unresolved_no_primary_metric leads with that evidence. tomlc99 (commit 62ce93ce) rejects the second control ("expect hex char" on a lowercase \u escape); libtoml targets TOML 0.4.0 and was not run. Zero selected is not evidence that no C TOML parser is used. A recheck on 2026-11-17 (Debian sourcemax and binary popcon tables, 40 and 57 toml hits, and all 1,981 Conan Center recipe names) again found no C TOML library, so the cell cannot reach 10 under the C primary metric or its Debian fallback; it stays at 0 rather than ranking unmetricked leads. Round 4 (2026-11-18) rechecked the toml-lang wiki C entries (toml-c, tomlc17, tomlc99, libtoml) against the Debian popcon source and binary tables (sourcemax SHA-256 7a460f12): none is packaged, so the cell still has no path with the primary metric or a Debian fallback and stays at 0. Round 5 (2026-11-18) checked tree-sitter grammars: Debian packages no TOML grammar, so the cell still has no C TOML library with a Debian count, and under the tree-sitter rule in PROTOCOL.md the harness would also have to merge dotted keys and tables and decode escapes itself. It stays at 0 (registry snapshot, round_5_tree_sitter).

[Ranking and search limits](../../../data/c/toml/ranking.md) · [Standard API inventory](../../../data/c/toml/standard.json)

## Third-party parsers

None verified in this pilot cell yet.

## Standard and runtime APIs

None verified in this pilot cell yet.
