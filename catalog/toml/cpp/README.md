# TOML / C++ — pilot

**Status:** pilot_three_selected_search_bounded; incomplete. 3 verified third-party paths, 0 verified standard APIs, 3 verified Docker harnesses.

Bounded TOML search captured 2026-11-17: 3 queries, 100 recorded hits (86 unique), at most 100 per query. 3 C++ TOML paths (toml++, toml11, cpptoml) print the exact typed tree for both valid controls and show scoped parser source coverage and stable, input-dependent AFL++ feedback (parser-only probes, function- and file-scoped allowlists, three identical repeats per control). The two lower ranks rest on very small counts: toml11 15 installations (0 recent, all no_files) and cpptoml 5 (0 recent). cpptoml 0.1.1 is a 2018 release that targets TOML 0.5.0 and needs <limits> included before its header on the pinned libstdc++; it passes both TOML 1.0.0 controls, which establish only that subset. No other C++ TOML parser appears in the Debian or Conan Center searches; libraries outside these surfaces are not counted. A recheck on 2026-11-17 (Debian sourcemax and binary popcon tables, 40 and 57 toml hits, and all 1,981 Conan Center recipe names) found no fourth C++ TOML library; r-cran-rcpptoml (1,539) is an R package that bundles toml++, not a C++ path. The cell therefore stays at 3 and cannot reach 10 on these surfaces. Two valid controls establish only the tested TOML 1.0.0 subset; malformed input, huge documents and TOML 1.1 features are untested. Round 4 (2026-11-18) looked up every C++ entry of the toml-lang wiki lists in the Debian popcon tables (sourcemax SHA-256 7a460f12): glaze 9.1.0 (source package glaze, 171, JSON-first multi-format library) is the only one packaged, and its documented schema-less TOML targets have no date-time alternative, so it stays a lead; erbsland-qt-toml, nullptr-0/toml and the tomlc17 C++ binding are not in Debian and have no primary metric. The cell stays at 3. Round 6 (2026-11-18) tried the toml-test-matrix list (its C++ entries are the selected toml++ and toml11 and the unpackaged nullptr-toml lead) and the sources.debian.org name search (41 source packages; the only C++ TOML libraries are the three selected). The cell stays at three.

[Ranking and search limits](../../../data/cpp/toml/ranking.md) · [Standard API inventory](../../../data/cpp/toml/standard.json)

## Third-party parsers

- [tomlplusplus](tomlplusplus/README.md) — verified Docker harness
- [toml11](toml11/README.md) — verified Docker harness
- [cpptoml](cpptoml/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
