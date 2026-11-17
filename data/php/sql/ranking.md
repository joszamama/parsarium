# PHP × SQL: pilot ranking

No path is verified yet, so nothing is ranked. Paths are ranked only among verified paths in this cell. The ceiling is ten, and the cell is not padded. The scope, controls and oracle are in [catalog/sql/PROTOCOL.md](../../../catalog/sql/PROTOCOL.md).

## Primary within-cell adoption metric

Packagist total downloads, captured 2026-11-17 ([snapshot](registry-snapshot.json)).

## Leads by the same metric

| Lead | Metric | Status | Parser family |
| --- | ---: | --- | --- |
| doctrine/sql-formatter | 216,519,891 | excluded | — |
| jdorn/sql-formatter | 120,134,108 | excluded | — |
| iamcal/sql-parser | 72,745,721 | excluded | iamcal/sql-parser |
| phpmyadmin/sql-parser | 55,800,144 | unresolved | phpMyAdmin hand-written lexer and parser |
| greenlion/php-sql-parser | 13,810,212 | unresolved | PHP-SQL-Parser |
| sqlftw/sqlftw | 169,733 | unresolved | SQLFTW |

Reasons are in [leads.json](leads.json). Standard and runtime findings are in [standard.json](standard.json).
