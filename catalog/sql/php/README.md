# SQL / PHP — pilot

**Status:** pilot_two_selected_search_bounded; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Two verified PHP SQL paths after a bounded Packagist search (three queries, 186 hits, 115 unique) and Packagist total downloads for 8 targeted leads, captured 2026-11-17. phpmyadmin/sql-parser 6.0.1 (55,800,144 total downloads) and greenlion/php-sql-parser v5.0.0 (13,810,212) parse both valid controls into structures that give the oracle summary. They are independent code bases. iamcal/sql-parser (72,745,721) ranks higher but parses only CREATE TABLE schemas, and the doctrine and jdorn packages are formatters. sqlftw/sqlftw and other leads are unverified, so this is not a top-ten ranking. greenlion treats the whole input as one statement. PDO and SQLite3 prepare are engine APIs with no syntax tree. Two valid controls establish only the tested dialect-neutral subset.

[Ranking and search limits](../../../data/php/sql/ranking.md) · [Standard API inventory](../../../data/php/sql/standard.json)

## Third-party parsers

- [phpmyadmin/sql-parser](phpmyadmin-sql-parser/README.md) — verified Docker harness
- [greenlion/php-sql-parser](greenlion-php-sql-parser/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
