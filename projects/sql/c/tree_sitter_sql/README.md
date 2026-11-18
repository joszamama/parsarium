# tree-sitter-sql — SQL / C

Pinned release: `0.3.11`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/c/tree-sitter-sql/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql c tree_sitter_sql
python3 parsarium.py run sql c tree_sitter_sql controls/sql/select-join.sql
python3 parsarium.py replay sql c tree_sitter_sql CORPUS_DIR runs/sql-tree_sitter_sql-replay
python3 parsarium.py afl build sql c tree_sitter_sql
python3 parsarium.py afl prepare sql c tree_sitter_sql runs/sql-tree_sitter_sql-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
