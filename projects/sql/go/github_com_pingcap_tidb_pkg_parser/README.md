# github.com/pingcap/tidb/pkg/parser — SQL / Go

Pinned release: `v0.0.0-20261117145351-1e84b3595a3e`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/go/github-com-pingcap-tidb-pkg-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql go github_com_pingcap_tidb_pkg_parser
python3 parsarium.py run sql go github_com_pingcap_tidb_pkg_parser controls/sql/select-join.sql
python3 parsarium.py replay sql go github_com_pingcap_tidb_pkg_parser CORPUS_DIR runs/sql-github_com_pingcap_tidb_pkg_parser-replay
python3 parsarium.py afl build sql go github_com_pingcap_tidb_pkg_parser
python3 parsarium.py afl prepare sql go github_com_pingcap_tidb_pkg_parser runs/sql-github_com_pingcap_tidb_pkg_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
