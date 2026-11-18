# SQL / Rust — pilot

**Status:** pilot_ten_selected_search_bounded; incomplete. 10 verified third-party paths, 0 verified standard APIs, 10 verified Docker harnesses.

Ten verified Rust SQL paths, the ceiling, after a bounded crates.io search (three queries, first 100 hits each, 300 hits, 250 unique) and recent-download metrics captured 2026-11-17; the snapshot hits were inspected in metric order. Each selected path parses both valid controls into its own AST, and the adapter's summary equals the hand-written oracle; families and metrics are in parsers.json. Two paths share the libpg_query family: pg_query and typedpg_pg_query (the latter with its own crate, build-time patches and vendored PostgreSQL 18.6 grammar copy). Downloads include transitive pulls through engines and bindings, and counts below 10,000 are weak adoption evidence. Forks of sqlparser-rs and sqlite3-parser, non-open-source licences and the predecessor sql-parse are excluded with evidence in leads.json; lower-ranked leads (oxisqlite-sqlite3-parser, turso_sqlite3_parser, banshee_parser) were not evaluated once the ceiling was reached, so this is not a definitive top-ten ranking. Two valid controls establish only the tested dialect-neutral subset.

[Ranking and search limits](../../../data/rust/sql/ranking.md) · [Standard API inventory](../../../data/rust/sql/standard.json)

## Third-party parsers

- [sqlparser](sqlparser/README.md) — verified Docker harness
- [pg_query](pg-query/README.md) — verified Docker harness
- [sqlite3-parser](sqlite3-parser/README.md) — verified Docker harness
- [polyglot-sql](polyglot-sql/README.md) — verified Docker harness
- [databend-common-ast](databend-common-ast/README.md) — verified Docker harness
- [qusql-parse](qusql-parse/README.md) — verified Docker harness
- [typedpg_pg_query](typedpg-pg-query/README.md) — verified Docker harness
- [spg-sql](spg-sql/README.md) — verified Docker harness
- [sqlglot-rust](sqlglot-rust/README.md) — verified Docker harness
- [nom-sql](nom-sql/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
