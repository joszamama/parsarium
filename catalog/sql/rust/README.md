# SQL / Rust — pilot

**Status:** pilot_one_selected_search_bounded; incomplete. 1 verified third-party paths, 0 verified standard APIs, 1 verified Docker harnesses.

One verified Rust SQL path after a bounded crates.io search (three queries, first 100 hits each, 300 hits, 250 unique) and recent-download metrics for 11 targeted leads, captured 2026-11-17. sqlparser 0.64.0 (18,971,518 90-day downloads) parses both valid controls with GenericDialect into ASTs that give the oracle summary. Its downloads include transitive pulls through DataFusion and other engines. pg_query (libpg_query FFI), sqlite3-parser and other leads are unverified, so this is not a top-ten ranking. sqlparser_derive, datafusion-sql and gluesql-core are sqlparser-rs family helpers or consumers, not separate parsers. Two valid controls establish only the tested dialect-neutral subset.

[Ranking and search limits](../../../data/rust/sql/ranking.md) · [Standard API inventory](../../../data/rust/sql/standard.json)

## Third-party parsers

- [sqlparser](sqlparser/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
