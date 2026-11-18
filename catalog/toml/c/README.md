# TOML / C — pilot

**Status:** pilot_one_selected_search_bounded; incomplete. 1 verified third-party paths, 0 verified standard APIs, 1 verified Docker harnesses.

Bounded TOML search captured 2026-11-17: 3 queries, 100 recorded hits (86 unique), at most 100 per query. Primary metric: no C TOML library appears in Debian popcon or Conan Center, so no C path has the primary metric or a Debian fallback of at least 1,000. A recheck on 2026-11-17 (Debian sourcemax and binary popcon tables, 40 and 57 toml hits, and all 1,981 Conan Center recipe names) found no C TOML library, and a 2026-11-18 lookup of the toml-lang wiki C entries (toml-c, tomlc17, tomlc99, libtoml) in the Debian popcon source and binary tables (sourcemax SHA-256 7a460f12) found none of them packaged. Tree-sitter grammars do not help either (registry snapshot, round_5_tree_sitter): Debian packages no TOML grammar, and under the tree-sitter rule in PROTOCOL.md the harness would also have to merge dotted keys and tables and decode escapes itself. Star fallback (2026-11-18): PROTOCOL.md lets C and C++ cells fill slots left empty after primary and Debian paths with pinned tagged releases of format-specific upstream repositories with at least 100 GitHub stars, ranked separately. Three GitHub repository searches (toml language:C, toml parser language:C, topic:toml language:C; first 100 hits by stars) found five repositories with at least 100 stars. tomlc17 R261116 (201 stars) was built from its pinned tag and printed the exact typed tree for both controls (1034 and 1105 tomlc17.c lines in the parser-only probe, 268/368 AFL++ tuples, 216 differ, three identical repeats); it is selected as a supplemental star path. toml-c (114 stars, tomlc99 fork, commit 6a38d404) also passed both valid controls with exact typed trees, parser coverage and stable AFL++ feedback, but has no tagged release, so the fallback does not apply and it stays a lead with that evidence. tomlc99 (664 stars, commit 62ce93ce) has no tagged release and rejects the second control ("expect hex char" on a lowercase \u escape). libtoml (125 stars) has no tagged release, targets TOML 0.4.0 and was not run. fwm is a Wayland compositor. Stars measure repository interest, not installations, and are not comparable with popcon values. The cell has one path and cannot reach 10 on these surfaces; a single selection is not evidence that no other C TOML parser is used.

[Ranking and search limits](../../../data/c/toml/ranking.md) · [Standard API inventory](../../../data/c/toml/standard.json)

## Third-party parsers

- [tomlc17](tomlc17/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
