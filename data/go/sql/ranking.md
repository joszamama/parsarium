# Go × SQL: pilot ranking

Four third-party paths are control verified against the hand-written oracle in [controls/sql/expected.json](../../../controls/sql/expected.json), with a pinned Docker harness, parser-source coverage and stable AFL++ feedback that differs between the two controls. Paths are ranked only among verified paths in this cell. The ceiling is ten, and the cell is not padded. The scope, controls and oracle are in [catalog/sql/PROTOCOL.md](../../../catalog/sql/PROTOCOL.md).

## Primary within-cell adoption metric

pkg.go.dev Imported by package count, captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [vitess.io/vitess/go/vt/sqlparser](https://pkg.go.dev/vitess.io/vitess@v0.24.5/go/vt/sqlparser#Parser.Parse) | v0.24.5 | 391 | `sqlparser.New(sqlparser.Options{}); Parser.SplitStatementToPieces and Parser.Parse(local SQL text) -> Statement`; dialect: MySQL (library default MySQL server version) | vitess MySQL grammar (goyacc sql.y) and tokenizer |
| 2 | [github.com/xwb1989/sqlparser](https://pkg.go.dev/github.com/xwb1989/sqlparser@v0.0.0-20180606152119-120387863bf2#Parse) | v0.0.0-20180606152119-120387863bf2 | 305 | `sqlparser.SplitStatementToPieces and sqlparser.Parse(local SQL text) -> Statement`; dialect: MySQL (vitess-derived grammar, no dialect option) | vitess MySQL grammar (2018 extracted fork, goyacc sql.y) and tokenizer |
| 3 | [github.com/pingcap/tidb/pkg/parser](https://pkg.go.dev/github.com/pingcap/tidb/pkg/parser@v0.0.0-20261117145351-1e84b3595a3e#Parser.Parse) | v0.0.0-20261117145351-1e84b3595a3e | 176 | `parser.New().Parse(local SQL text, "", "") -> []ast.StmtNode`; dialect: MySQL (TiDB parser, default charset and collation) | TiDB MySQL grammar (goyacc parser.y) and lexer |
| 4 | [github.com/AfterShip/clickhouse-sql-parser/parser](https://pkg.go.dev/github.com/AfterShip/clickhouse-sql-parser@v0.5.7/parser#Parser.ParseStmts) | v0.5.7 | 13 | `parser.NewParser(local SQL text).ParseStmts() -> []parser.Expr`; dialect: ClickHouse (no dialect option) | clickhouse-sql-parser hand-written recursive-descent parser and lexer |

Receipts: [vitess.io/vitess/go/vt/sqlparser](../../../projects/sql/go/vitess_io_vitess_go_vt_sqlparser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/go/vitess_io_vitess_go_vt_sqlparser/differential.json), [github.com/xwb1989/sqlparser](../../../projects/sql/go/github_com_xwb1989_sqlparser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/go/github_com_xwb1989_sqlparser/differential.json), [github.com/pingcap/tidb/pkg/parser](../../../projects/sql/go/github_com_pingcap_tidb_pkg_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/go/github_com_pingcap_tidb_pkg_parser/differential.json), [github.com/AfterShip/clickhouse-sql-parser/parser](../../../projects/sql/go/github_com_aftership_clickhouse_sql_parser_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/go/github_com_aftership_clickhouse_sql_parser_parser/differential.json).

## Leads by the same metric

| Lead | Metric | Status | Parser family |
| --- | ---: | --- | --- |
| github.com/pingcap/tidb/ast | 3,737 | excluded | TiDB MySQL grammar |
| github.com/cockroachdb/cockroach/pkg/sql/parser | 1,972 | unresolved | CockroachDB PostgreSQL-compatible grammar |
| github.com/pingcap/tidb/parser | 1,190 | unresolved | TiDB MySQL grammar (goyacc) |
| vitess.io/vitess/go/vt/sqlparser | 391 | selected | vitess MySQL grammar (goyacc) |
| github.com/pingcap/parser | 385 | unresolved_blocked | TiDB MySQL grammar (goyacc) |
| github.com/xwb1989/sqlparser | 305 | selected | vitess MySQL grammar (extracted fork) |
| github.com/pingcap/tidb/pkg/parser | 176 | selected | TiDB MySQL grammar (goyacc) |
| github.com/blastrain/vitess-sqlparser/sqlparser | 88 | unresolved | vitess MySQL grammar (fork) |
| github.com/pganalyze/pg_query_go/v6 | 54 | unresolved | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| github.com/auxten/postgresql-parser/pkg/sql/parser | 22 | unresolved | CockroachDB PostgreSQL-compatible grammar |
| github.com/rqlite/sql | 20 | unresolved | rqlite/sql hand-written parser |
| github.com/cockroachdb/cockroachdb-parser/pkg/sql/parser | 13 | unresolved | CockroachDB PostgreSQL-compatible grammar |
| github.com/AfterShip/clickhouse-sql-parser/parser | 13 | selected | clickhouse-sql-parser hand-written |
| github.com/akito0107/xsqlparser | 7 | unresolved | sqlparser-rs port |
| github.com/krasun/gosqlparser | 1 | unresolved | gosqlparser |

Reasons are in [leads.json](leads.json). Standard and runtime findings are in [standard.json](standard.json).
