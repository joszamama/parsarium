# TOML / PHP — pilot

**Status:** pilot_two_selected_search_bounded; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Bounded TOML search captured 2026-11-17: 2 queries, 183 recorded hits (162 unique), at most 100 per query. Two paths are verified on both valid controls: internal/toml 1.1.3 and php-collective/toml 0.1.5. Neither array API keeps the TOML scalar kinds (internal/toml returns local date-times and local dates as DateTimeImmutable like offset date-times and local times as strings; php-collective/toml returns all three local kinds as strings), so each harness reads the kinds from the library's documented AST value nodes and requires the AST walk to place exactly the values the library's own array assembly returns. The two most downloaded leads failed the typed-scalars control: yosymfony/toml v1.0.4 (TOML 0.4.0) rejects the hexadecimal integer, and devium/toml 1.1.1 stores the local time fraction .25 as 25 milliseconds. Round 2 ran six more: jamesmoss/toml 1.1.1, leonelquinteros/php-toml v1.1.1 and zidizei/toml-php 0.3.0 (old drafts) reject inline tables or hexadecimal integers; app-hive/toml 0.0.2 (with its undeclared ext-gmp) and dayvsonspacca/psl-toml v1.0.5 (with its undeclared ext-bcmath) lose the date-time kinds or mis-parse values; petalbranch/toml v1.2.0 loses date-time kinds in its array API, and a harness over its typed node tree was not built. 13 leads remain unresolved, 5 of them not run (no tagged release, or a TOML 0.4 fork with 0 downloads). Packagist lifetime downloads measure historical adoption, not TOML parsing frequency. Two valid controls establish only the tested TOML 1.0.0 subset; empty tables (indistinguishable from empty arrays in PHP), malformed input, huge documents and TOML 1.1 features are untested.

[Ranking and search limits](../../../data/php/toml/ranking.md) · [Standard API inventory](../../../data/php/toml/standard.json)

## Third-party parsers

- [internal/toml](internal-toml/README.md) — verified Docker harness
- [php-collective/toml](php-collective-toml/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
