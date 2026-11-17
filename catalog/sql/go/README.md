# SQL / Go — pilot

**Status:** pilot_one_selected_search_bounded; incomplete. 1 verified third-party paths, 0 verified standard APIs, 1 verified Docker harnesses.

One verified Go SQL path after a bounded pkg.go.dev search (three queries, first 100 hits each, 300 hits, 274 unique) and Imported-by counts for 12 targeted leads, captured 2026-11-17. vitess.io/vitess/go/vt/sqlparser v0.24.5 (391 importers) parses both valid controls with its default MySQL version into ASTs that give the oracle summary. The search snippets list higher importer counts for github.com/pingcap/tidb/ast (3,737, AST types only), github.com/cockroachdb/cockroach/pkg/sql/parser (1,972, inside the full CockroachDB module) and github.com/pingcap/tidb/parser (1,190, older in-repo TiDB parser path); these and pingcap/parser, xwb1989/sqlparser, pg_query_go and other leads are unverified, so this is not a top-ten ranking. database/sql has no SQL parser. Two valid controls establish only the tested dialect-neutral subset.

[Ranking and search limits](../../../data/go/sql/ranking.md) · [Standard API inventory](../../../data/go/sql/standard.json)

## Third-party parsers

- [vitess.io/vitess/go/vt/sqlparser](vitess-io-vitess-go-vt-sqlparser/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
