# SQL / JavaScript — pilot

**Status:** pilot_two_selected_search_bounded; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Two verified JavaScript SQL paths after a bounded npm search (three queries, first 100 hits each, 259 hits, 236 unique) and npm last-month downloads for 15 targeted leads, captured 2026-11-17. node-sql-parser 5.4.0 (13,709,122) and pgsql-ast-parser 12.0.2 (7,717,032) parse both valid controls into their own ASTs, which give the oracle summary. node-sql-parser ships minified, so its line coverage is mapped through the package source map. libpg-query 18.2.4 (11,829,732) ranks between them but runs libpg_query compiled to WebAssembly; V8 coverage does not report C source lines inside the module, so the parser-source coverage gate cannot be met with this harness and it stays a lead. sql-formatter (29,933,061) is a formatter. Other leads are unverified, so this is not a top-ten ranking. node:sqlite prepare is an engine API with no syntax tree. Two valid controls establish only the tested dialect-neutral subset.

[Ranking and search limits](../../../data/javascript/sql/ranking.md) · [Standard API inventory](../../../data/javascript/sql/standard.json)

## Third-party parsers

- [node-sql-parser](node-sql-parser/README.md) — verified Docker harness
- [pgsql-ast-parser](pgsql-ast-parser/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
