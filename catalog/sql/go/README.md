# SQL / Go — pilot

**Status:** pilot_ten_selected_search_bounded; incomplete. 10 verified third-party paths, 0 verified standard APIs, 10 verified Docker harnesses.

Ten verified Go SQL paths after a bounded pkg.go.dev search (three queries, first 100 hits each, 300 hits, 274 unique) and Imported-by counts for 12 targeted leads, captured 2026-11-17: vitess.io/vitess/go/vt/sqlparser (391), github.com/xwb1989/sqlparser (305), github.com/pingcap/tidb/pkg/parser (176), github.com/blastrain/vitess-sqlparser/sqlparser (88), github.com/pganalyze/pg_query_go/v6 (54), github.com/auxten/postgresql-parser/pkg/sql/parser (22), github.com/rqlite/sql (20), github.com/AfterShip/clickhouse-sql-parser/parser (13), github.com/cockroachdb/cockroachdb-parser/pkg/sql/parser (13), github.com/akito0107/xsqlparser (7). Each parses both valid controls into an AST that gives the oracle summary; untagged modules are pinned to proxy pseudo-versions. Higher importer counts in the search snippets belong to github.com/pingcap/tidb/ast (3,737, AST types only), github.com/cockroachdb/cockroach/pkg/sql/parser (1,972, not importable as a library) and github.com/pingcap/tidb/parser (1,190, predecessor path of the selected TiDB parser); remaining leads and blockers are in leads.json, so this is not a definitive top-ten ranking. database/sql has no SQL parser. Two valid controls establish only the tested dialect-neutral subset.

[Ranking and search limits](../../../data/go/sql/ranking.md) · [Standard API inventory](../../../data/go/sql/standard.json)

## Third-party parsers

- [vitess.io/vitess/go/vt/sqlparser](vitess-io-vitess-go-vt-sqlparser/README.md) — verified Docker harness · [source repository](<https://github.com/vitessio/vitess>) · [pkg.go.dev](<https://pkg.go.dev/vitess.io/vitess/go/vt/sqlparser>)
- [github.com/xwb1989/sqlparser](github-com-xwb1989-sqlparser/README.md) — verified Docker harness · [source repository](<https://github.com/xwb1989/sqlparser>) · [pkg.go.dev](<https://pkg.go.dev/github.com/xwb1989/sqlparser>)
- [github.com/pingcap/tidb/pkg/parser](github-com-pingcap-tidb-pkg-parser/README.md) — verified Docker harness · [source repository](<https://github.com/pingcap/tidb>) · [pkg.go.dev](<https://pkg.go.dev/github.com/pingcap/tidb/pkg/parser>)
- [github.com/blastrain/vitess-sqlparser/sqlparser](github-com-blastrain-vitess-sqlparser-sqlparser/README.md) — verified Docker harness · [source repository](<https://github.com/blastrain/vitess-sqlparser>) · [pkg.go.dev](<https://pkg.go.dev/github.com/blastrain/vitess-sqlparser/sqlparser>)
- [github.com/pganalyze/pg_query_go/v6](github-com-pganalyze-pg-query-go-v6/README.md) — verified Docker harness · [source repository](<https://github.com/pganalyze/pg_query_go>) · [pkg.go.dev](<https://pkg.go.dev/github.com/pganalyze/pg_query_go/v6>)
- [github.com/auxten/postgresql-parser/pkg/sql/parser](github-com-auxten-postgresql-parser-pkg-sql-parser/README.md) — verified Docker harness · [source repository](<https://github.com/auxten/postgresql-parser>) · [pkg.go.dev](<https://pkg.go.dev/github.com/auxten/postgresql-parser/pkg/sql/parser>)
- [github.com/rqlite/sql](github-com-rqlite-sql/README.md) — verified Docker harness · [source repository](<https://github.com/rqlite/sql>) · [pkg.go.dev](<https://pkg.go.dev/github.com/rqlite/sql>)
- [github.com/AfterShip/clickhouse-sql-parser/parser](github-com-aftership-clickhouse-sql-parser-parser/README.md) — verified Docker harness · [source repository](<https://github.com/AfterShip/clickhouse-sql-parser>) · [pkg.go.dev](<https://pkg.go.dev/github.com/AfterShip/clickhouse-sql-parser/parser>)
- [github.com/cockroachdb/cockroachdb-parser/pkg/sql/parser](github-com-cockroachdb-cockroachdb-parser-pkg-sql-parser/README.md) — verified Docker harness · [source repository](<https://github.com/cockroachdb/cockroachdb-parser>) · [pkg.go.dev](<https://pkg.go.dev/github.com/cockroachdb/cockroachdb-parser/pkg/sql/parser>)
- [github.com/akito0107/xsqlparser](github-com-akito0107-xsqlparser/README.md) — verified Docker harness · [source repository](<https://github.com/akito0107/xsqlparser>) · [pkg.go.dev](<https://pkg.go.dev/github.com/akito0107/xsqlparser>)

## Standard and runtime APIs

None verified in this pilot cell yet.
