# SQL / C — pilot

**Status:** pilot_two_selected_search_bounded; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Two verified C SQL paths after a bounded Debian popcon source-name search (names containing 'sql', first 100 of 229 by rank) plus targeted lookups, captured 2026-11-17 from the pinned popcon snapshot. libgda 5.2.10 (Debian source libgda5, 2,105 installations) parses both valid controls with its generic Lemon-generated GdaSqlParser into a GdaSqlStatement tree, and libpg_query 18.1.0 (Debian source libpg-query, 41) parses them with the PostgreSQL 18 grammar; both trees give the oracle summary. sqlite3, sqlcipher and postgresql-18 rank higher but are engines or a server without a library syntax-tree API. Both popcon counts are small or library-wide (libgda's covers the whole data-access library) and reflect packaged installs, not use of SQL parsing. No other C source package in the snapshot was found with a documented SQL syntax-tree API, so the cell has two paths, not ten. Two valid controls establish only the tested dialect-neutral subset.

[Ranking and search limits](../../../data/c/sql/ranking.md) · [Standard API inventory](../../../data/c/sql/standard.json)

## Third-party parsers

- [libgda](libgda/README.md) — verified Docker harness
- [libpg_query](libpg-query/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
