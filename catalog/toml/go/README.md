# TOML / Go — pilot

**Status:** pilot_two_selected_search_bounded; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Bounded TOML search captured 2026-11-17: 3 pkg.go.dev queries, 300 recorded hits (263 unique), at most 100 per query. Two Go TOML paths pass both valid controls with the exact typed tree, parser-source coverage and stable AFL++ feedback: BurntSushi/toml v1.6.0 (38,240 Imported by; 585 own lines on service-config, 385/420 AFL++ tuples, 169 differ) and pelletier/go-toml/v2 v2.4.3 (1,986; 739 lines, 482/480 tuples, 342 differ). Each uses its own lexer/parser; they share no code. Higher-ranked pelletier/go-toml v1.9.5 (3,687) fails the typed-scalars control on a local date followed by a newline, and naoina/toml v0.1.1 (2,071) rejects the TOML 0.5 octal integer 0o755; both stay leads, so ranks cover verified paths only. 6 parser leads remain unresolved. BurntSushi/toml marks local date-times, dates and times only by the names of fixed time zones it attaches to time.Time (datetime-local, date-local, time-local), not by distinct Go types. Two valid controls establish only the tested TOML 1.0.0 subset; malformed input, huge documents and TOML 1.1 features are untested.

[Ranking and search limits](../../../data/go/toml/ranking.md) · [Standard API inventory](../../../data/go/toml/standard.json)

## Third-party parsers

- [github.com/BurntSushi/toml](github-com-burntsushi-toml/README.md) — verified Docker harness
- [github.com/pelletier/go-toml/v2](github-com-pelletier-go-toml-v2/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
