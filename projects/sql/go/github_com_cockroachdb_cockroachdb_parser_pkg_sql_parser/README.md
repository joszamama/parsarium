# github.com/cockroachdb/cockroachdb-parser/pkg/sql/parser — SQL / Go

Pinned release: `v0.25.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/go/github-com-cockroachdb-cockroachdb-parser-pkg-sql-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql go github_com_cockroachdb_cockroachdb_parser_pkg_sql_parser
python3 parsarium.py run sql go github_com_cockroachdb_cockroachdb_parser_pkg_sql_parser controls/sql/select-join.sql
python3 parsarium.py replay sql go github_com_cockroachdb_cockroachdb_parser_pkg_sql_parser CORPUS_DIR runs/sql-github_com_cockroachdb_cockroachdb_parser_pkg_sql_parser-replay
python3 parsarium.py afl build sql go github_com_cockroachdb_cockroachdb_parser_pkg_sql_parser
python3 parsarium.py afl prepare sql go github_com_cockroachdb_cockroachdb_parser_pkg_sql_parser runs/sql-github_com_cockroachdb_cockroachdb_parser_pkg_sql_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
