# SQL / Rust — pilot

**Status:** pilot_nine_selected_search_bounded; incomplete. 9 verified third-party paths, 0 verified standard APIs, 9 verified Docker harnesses.

Nine verified Rust SQL paths after a bounded crates.io search (three queries, first 100 hits each, 300 hits, 250 unique) and recent-download metrics captured 2026-11-17; round 2 inspected the snapshot hits in metric order. Each selected path parses both valid controls into its own AST, and the adapter's summary equals the hand-written oracle; families and metrics are in parsers.json. Downloads include transitive pulls through engines and bindings, and counts below 10,000 are weak adoption evidence. Forks of sqlparser-rs and sqlite3-parser, non-open-source licences and the predecessor sql-parse are excluded with evidence in leads.json; unverified leads remain, so this is not a definitive top-ten ranking. Two valid controls establish only the tested dialect-neutral subset.

[Ranking and search limits](../../../data/rust/sql/ranking.md) · [Standard API inventory](../../../data/rust/sql/standard.json)

## Third-party parsers

- [sqlparser](sqlparser/README.md) — verified Docker harness
- [pg_query](pg-query/README.md) — verified Docker harness
- [sqlite3-parser](sqlite3-parser/README.md) — verified Docker harness
- [polyglot-sql](polyglot-sql/README.md) — verified Docker harness
- [databend-common-ast](databend-common-ast/README.md) — verified Docker harness
- [qusql-parse](qusql-parse/README.md) — verified Docker harness
- [spg-sql](spg-sql/README.md) — verified Docker harness
- [sqlglot-rust](sqlglot-rust/README.md) — verified Docker harness
- [nom-sql](nom-sql/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
