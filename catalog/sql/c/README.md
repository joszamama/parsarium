# SQL / C — pilot

**Status:** pilot_three_selected_search_bounded; incomplete. 3 verified third-party paths, 0 verified standard APIs, 3 verified Docker harnesses.

Three verified C SQL paths after a bounded Debian popcon source-name search (names containing 'sql', first 100 of 229 by rank) plus targeted lookups, captured 2026-11-17 from the pinned popcon snapshot. libgda 5.2.10 (Debian source libgda5, 2,105 installations) parses both valid controls with its generic Lemon-generated GdaSqlParser into a GdaSqlStatement tree, and libpg_query 18.1.0 (Debian source libpg-query, 41) parses them with the PostgreSQL 18 grammar; both trees give the oracle summary. sqlite3, sqlcipher and postgresql-18 rank higher but are engines or a server without a library syntax-tree API. Both popcon counts are small or library-wide (libgda's covers the whole data-access library) and reflect packaged installs, not use of SQL parsing. Round 3 (2026-11-18) checked further source packages of the same pinned snapshot outside the first 100 'sql' hits (mariadb, unixodbc, spatialite, freetds, psqlodbc, mdbtools; C++ candidates are in the C++ cell): they are a server and client, a driver manager, drivers, a SQLite extension, or a grammar without JOIN, GROUP BY or INSERT (libmdbsql), with evidence in leads.json. No other C source package in the snapshot was found with a documented SQL syntax-tree API, and no unranked C path exists for the Debian development-package fallback, so after round 3 the cell stopped at two paths; adding more would need a different metric (GitHub stars are allowed only in PLY cells). Two valid controls establish only the tested dialect-neutral subset. Round 4 (2026-11-18) looked up tree-sitter grammar sources in the same pinned snapshot and added tree-sitter-sql 0.3.11 (Debian source tree-sitter-sql, 8 installations, rank 3 of 3): the DerekStride grammar (generated parser.c and scanner.c, byte-identical to Debian 0.3.11-1) on the tree-sitter 0.26.11 C runtime builds a concrete syntax tree that gives the oracle summary for both controls. Its count is the weakest in the cell and measures the only binary package of that source, the Python binding python3-tree-sitter-sql, not C use; tree-sitter is error-tolerant, so the adapter rejects trees with ERROR or MISSING nodes. Other round-4 routes found no further path: the remaining snapshot lookups (tree-sitter runtime, virtuoso-opensource, cowsql, dqlite, mydumper, sqliteodbc, pgpool2, tarantool, libcypher-parser) are a grammar-less runtime, engines, middleware with an internal PostgreSQL parser copy, a backup tool, a driver or a Cypher parser; vcpkg and Conan Center list no C SQL parser besides libpg-query; and the GitHub search 'sql parser language:C' (discovery only) found sqliteai/liteparser, a C SQLite-grammar AST library with no Debian, vcpkg or Conan package and therefore no admissible metric (recorded as unresolved_no_primary_metric). The cell stops at three paths, not ten.

[Ranking and search limits](../../../data/c/sql/ranking.md) · [Standard API inventory](../../../data/c/sql/standard.json)

## Third-party parsers

- [libgda](libgda/README.md) — verified Docker harness
- [libpg_query](libpg-query/README.md) — verified Docker harness
- [tree-sitter-sql](tree-sitter-sql/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
