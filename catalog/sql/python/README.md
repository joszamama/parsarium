# SQL / Python — pilot

**Status:** pilot_two_selected_search_bounded; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Two verified Python SQL paths after a bounded PyPI Simple index name search (five normalized-name queries, all 41 hits kept) and PyPI Stats metrics for 14 targeted leads, captured 2026-11-17. sqlparse 0.6.1 (125,550,021 last-month downloads) is a non-validating parser: its grouped token tree gives the oracle summary for both valid controls, but it accepts invalid SQL, and its downloads mostly reflect Django use for formatting and splitting. sqlglot 30.33.0 (91,735,974) runs its pure-Python tokenizer and parser with the default dialect; the optional sqlglotc/sqlglotrs accelerators are not installed. The remaining unresolved leads (sqlfluff, pglast, sqloxide, mo-sql-parsing and others) are unverified, so this is not a top-ten ranking. CPython sqlite3 is an engine binding with no syntax tree and is recorded, not counted. Two valid controls establish only the tested dialect-neutral subset.

[Ranking and search limits](../../../data/python/sql/ranking.md) · [Standard API inventory](../../../data/python/sql/standard.json)

## Third-party parsers

- [sqlparse](sqlparse/README.md) — verified Docker harness
- [sqlglot](sqlglot/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
