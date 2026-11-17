# SQL / PHP — pilot

**Status:** pilot_five_selected_search_bounded; incomplete. 5 verified third-party paths, 0 verified standard APIs, 5 verified Docker harnesses.

Five verified PHP SQL paths after a bounded Packagist search (7 queries, 284 hits, 165 unique; round 1 on 2026-11-17 used three queries, round 2 added four) and Packagist total downloads for 35 targeted leads, captured 2026-11-17. phpmyadmin/sql-parser 6.0.1, greenlion/php-sql-parser v5.0.0, soundintheory/php-sql-parser 1.0, sad_spirit/pg_builder v3.3.1 and crodas/sql-parser v0.1.5 parse both valid controls into structures that give the oracle summary. soundintheory is a 2013 fork of the Google Code predecessor of greenlion (shared PHP-SQL-Parser lineage, separate monolithic code: 54.3% of its normalized statements occur in greenlion v5.0.0). Later greenlion forks (manticoresoftware, tsukasa, processfast, aitradeinc, michabbb) share 84-99.5% of normalized statements with greenlion and are excluded as near-identical forks or older snapshots; this cut-off is a curation judgment. crodas/sql-parser has a weak metric (2,490 lifetime downloads). The libpg_query PHP extension flow-php/pg-query-ext and its consumer flow-php/postgresql rank above crodas but stay runnability leads: their parser is native C and needs a native coverage and AFL++ PHP-runtime build that was not done in this round. sqlftw/sqlftw is proprietary. iamcal/sql-parser ranks higher but parses only CREATE TABLE schemas, and the doctrine, jdorn and nilportugues packages are formatters. This is not a top-ten ranking. greenlion and soundintheory treat the whole input as one statement; pg_builder parses one statement per call, so its adapter cuts the input at its own Lexer's ';' tokens. PDO and SQLite3 prepare are engine APIs with no syntax tree. Two valid controls establish only the tested dialect-neutral subset.

[Ranking and search limits](../../../data/php/sql/ranking.md) · [Standard API inventory](../../../data/php/sql/standard.json)

## Third-party parsers

- [phpmyadmin/sql-parser](phpmyadmin-sql-parser/README.md) — verified Docker harness
- [greenlion/php-sql-parser](greenlion-php-sql-parser/README.md) — verified Docker harness
- [soundintheory/php-sql-parser](soundintheory-php-sql-parser/README.md) — verified Docker harness
- [sad_spirit/pg_builder](sad-spirit-pg-builder/README.md) — verified Docker harness
- [crodas/sql-parser](crodas-sql-parser/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
