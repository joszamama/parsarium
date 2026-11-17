# TOML / Python — pilot

**Status:** pilot_two_selected_search_bounded; incomplete. 2 verified third-party paths, 1 verified standard APIs, 2 verified Docker harnesses.

Bounded TOML search captured 2026-11-17: 1 query, 100 recorded hits (100 unique), at most 100 per query; the PyPI Simple index has no relevance order and the name filter matches unrelated names, so the leads come from targeted lookups. Two third-party paths pass both valid controls with exact hand-written typed trees, parser-scoped Python line coverage and AFL++ feedback: tomlkit 0.15.2 (591,365,129 PyPI Stats last-month downloads; 845 package lines, 408 in parser.py; controls differ by 401 AFL++ tuples) and tomli 2.5.0 (263,305,223; 284 lines, 259 in _parser.py; controls differ by 137 tuples), three identical runs per control each. tomli is the same code family as the standard tomllib API (a vendored copy), so the two are not independent; the hand-written trees are tomli's independent check. Only tomli's pure-Python wheel is measured, not its mypyc-compiled wheels. tomlkit is an independent style-preserving parser; its downloads mostly reflect Poetry and other tool installs. toml 0.10.2 (145,147,540) fails typed-scalars: it drops the fractional seconds of the local time 00:32:00.25. rtoml 0.14.0 (1,380,894; Rust toml crate via PyO3), pytomlpp 1.1.0 (43,243; C++ toml++ via pybind11, linux/amd64 wheel only) and toml-rs 0.4.3 (18,062; Rust parser from a git branch via PyO3) give both exact typed trees, but their parsers are compiled native code that Python line coverage and the Python AFL++ bridge cannot reach; they stay leads until a source build with native coverage and AFL++ instrumentation exists. pytoml 0.1.21 (337,081) rejects the hexadecimal integer and qtoml 0.3.1 (2,002) the fractional-second offset date-time of typed-scalars. The standard tomllib API passed both controls on a host run. Two valid controls establish only the tested TOML 1.0.0 subset; malformed input, huge documents and TOML 1.1 features are untested.

[Ranking and search limits](../../../data/python/toml/ranking.md) · [Standard API inventory](../../../data/python/toml/standard.json)

## Third-party parsers

- [tomlkit](tomlkit/README.md) — verified Docker harness
- [tomli](tomli/README.md) — verified Docker harness
- [rtoml](rtoml/README.md) — verified API path

## Standard and runtime APIs

- [tomllib.load(local binary file)](standard/tomllib-load-local-binary-file/README.md) — verified API path
