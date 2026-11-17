# SQL / C++ — pilot

**Status:** pilot_one_selected_search_bounded; incomplete. 1 verified third-party paths, 0 verified standard APIs, 1 verified Docker harnesses.

One verified C++ SQL path after the shared Debian popcon source-name search (names containing 'sql', first 100 of 229 by rank) plus round-2 targeted lookups in the same pinned snapshot (duckdb, hsql/hyrise, gdal, kdb, libreoffice, sqlitebrowser, sqlitestudio, antlr4-cpp-runtime, soci, poco). DuckDB 2.0.0 (Debian source duckdb, 40 installations) parses both valid controls with its built-in PEG grammar through duckdb::Parser, without a database or client context, into SQLStatement trees that give the oracle summary; the adapter reports DuckDB's count_star node for COUNT(*) as count. Higher-ranked C++ sources are wrappers, applications with internal parsers, a runtime without a grammar, or parsers that cannot read the INSERT control or need a connection (GDAL OGR SQL, KDb). hsql has a documented AST API but no Debian source package, so it has no value for the primary metric. The popcon count is very small and counts installs of the whole engine, not use of its parser. DuckDB's parser is a public header of an engine whose C++ API is described upstream as internal. Two valid controls establish only the tested dialect-neutral subset.

[Ranking and search limits](../../../data/cpp/sql/ranking.md) · [Standard API inventory](../../../data/cpp/sql/standard.json)

## Third-party parsers

- [duckdb](duckdb/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
