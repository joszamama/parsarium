# TOML / C — pilot

**Status:** pilot_search_bounded_none_selected; incomplete. 0 verified third-party paths, 0 verified standard APIs, 0 verified Docker harnesses.

Bounded TOML search captured 2026-11-17: 3 queries, 100 recorded hits (86 unique), at most 100 per query. No C TOML library appears in Debian popcon or Conan Center, so no C path has the primary metric or a Debian fallback of at least 1,000, and none is selected. tomlc17 R261116 and toml-c (tomlc99 fork, commit 6a38d404) passed both valid controls with exact typed trees, parser coverage and stable AFL++ feedback; they stay unresolved_no_primary_metric leads with that evidence. tomlc99 (commit 62ce93ce) rejects the second control ("expect hex char" on a lowercase \u escape); libtoml targets TOML 0.4.0 and was not run. Zero selected is not evidence that no C TOML parser is used.

[Ranking and search limits](../../../data/c/toml/ranking.md) · [Standard API inventory](../../../data/c/toml/standard.json)

## Third-party parsers

None verified in this pilot cell yet.

## Standard and runtime APIs

None verified in this pilot cell yet.
