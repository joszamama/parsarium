# PHP × SQL: pilot ranking

Five third-party paths are control verified against the hand-written oracle in [controls/sql/expected.json](../../../controls/sql/expected.json), with a pinned Docker harness, parser-source coverage and stable AFL++ feedback that differs between the two controls. Paths are ranked only among verified paths in this cell. The ceiling is ten, and the cell is not padded. The scope, controls and oracle are in [catalog/sql/PROTOCOL.md](../../../catalog/sql/PROTOCOL.md).

## Primary within-cell adoption metric

Packagist total downloads, captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [phpmyadmin/sql-parser](https://github.com/phpmyadmin/sql-parser/blob/6.0.1/README.md#parsing) | 6.0.1 | 55,800,144 | `new PhpMyAdmin\SqlParser\Parser(local SQL text, strict: true) -> statements[]`; dialect: MySQL (library default context) | phpMyAdmin sql-parser hand-written lexer and statement parser |
| 2 | [greenlion/php-sql-parser](https://github.com/greenlion/PHP-SQL-Parser/blob/7a4701b71f7786e8518a9412f3c552ae4550d314/README.md) | v5.0.0 | 13,810,212 | `(new PHPSQLParser\PHPSQLParser())->parse(local SQL text) -> clause-keyed array parse tree`; dialect: MySQL-oriented (no dialect option) | PHP-SQL-Parser lexer and clause processors (nested array parse tree) |
| 3 | [soundintheory/php-sql-parser](https://github.com/soundintheory/php-sql-parser/blob/dcb81216a13be124d21711b8fefb6e80db7af472/README.md) | 1.0 | 599,598 | `(new PHPSQL\Parser())->parse(local SQL text) -> clause-keyed array parse tree`; dialect: MySQL-oriented (no dialect option) | PHP-SQL-Parser lineage (2013 PSR-0 fork of the Google Code php-sql-parser; shared family with greenlion/php-sql-parser) |
| 4 | [sad_spirit/pg_builder](https://github.com/sad-spirit/pg-builder/blob/2a1ff9bf16b014f37af1fce1c4b9db53782fe7f6/README.md) | v3.3.1 | 76,924 | `(new sad_spirit\pg_builder\StatementFactory())->createFromString(local SQL text) -> Statement AST`; dialect: PostgreSQL (the only dialect; default Lexer options) | pg_builder hand-written PostgreSQL lexer and recursive-descent parser (typed AST) |
| 5 | [crodas/sql-parser](https://github.com/crodas/SQLParser/blob/a0241cb8755ed36b2a0d0812503ee71abfbe52ac/README.md) | v0.1.5 | 2,490 | `(new SQLParser())->parse(local SQL text) -> SQL\Statement objects`; dialect: MySQL-oriented (no dialect option) | crodas SQLParser Lemon-generated LALR parser (SQL\Statement objects) |

Receipts: [phpmyadmin/sql-parser](../../../projects/sql/php/phpmyadmin_sql_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/php/phpmyadmin_sql_parser/differential.json), [greenlion/php-sql-parser](../../../projects/sql/php/greenlion_php_sql_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/php/greenlion_php_sql_parser/differential.json), [soundintheory/php-sql-parser](../../../projects/sql/php/soundintheory_php_sql_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/php/soundintheory_php_sql_parser/differential.json), [sad_spirit/pg_builder](../../../projects/sql/php/sad_spirit_pg_builder/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/php/sad_spirit_pg_builder/differential.json), [crodas/sql-parser](../../../projects/sql/php/crodas_sql_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/php/crodas_sql_parser/differential.json).

## Leads by the same metric

| Lead | Metric | Status | Parser family |
| --- | ---: | --- | --- |
| doctrine/sql-formatter | 216,519,891 | excluded | — |
| jdorn/sql-formatter | 120,134,108 | excluded | — |
| iamcal/sql-parser | 72,745,721 | excluded | iamcal/sql-parser |
| phpmyadmin/sql-parser | 55,800,144 | selected | phpMyAdmin hand-written lexer and parser |
| greenlion/php-sql-parser | 13,810,212 | selected | PHP-SQL-Parser |
| nilportugues/sql-query-formatter | 1,321,928 | excluded | — |
| staabm/sql-parser-util | 1,271,938 | excluded | — |
| soundintheory/php-sql-parser | 599,598 | selected | PHP-SQL-Parser lineage (2013 fork; shared with greenlion) |
| jasny/persist-sql-query | 578,756 | excluded | — |
| sqlftw/sqlftw | 169,733 | excluded | SQLFTW |
| sad_spirit/pg_builder | 76,924 | selected | pg_builder hand-written PostgreSQL parser |
| getdkan/sql-parser | 66,786 | excluded | DKAN state-machine validator |
| manticoresoftware/php-sql-parser | 63,809 | excluded | PHP-SQL-Parser (greenlion fork) |
| marcocesarato/sqlparser | 50,961 | excluded | — |
| flow-php/postgresql | 45,374 | unresolved_runnability_blocker | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| intersvyaz/yii2-sqlparser | 30,004 | excluded | — |
| jasny/dbquery-mysql | 27,582 | excluded | — |
| flow-php/pg-query-ext | 18,762 | unresolved_runnability_blocker | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| tsukasa/php-sql-parser | 14,933 | excluded | PHP-SQL-Parser (greenlion fork) |
| udan11/sql-parser | 9,823 | excluded | phpMyAdmin hand-written lexer and parser |
| processfast/php-sql-parser | 8,250 | excluded | PHP-SQL-Parser (greenlion fork) |
| liquipedia/sqllint | 5,398 | excluded | phpMyAdmin hand-written lexer and parser |
| crodas/sql-parser | 2,490 | selected | crodas SQLParser Lemon-generated parser |
| michabbb/php-sql-parser | 2,299 | excluded | PHP-SQL-Parser (greenlion fork) |
| fmizzell/sql-parser | 1,367 | excluded | DKAN state-machine validator |
| aitradeinc/php-sql-parser | 399 | excluded | PHP-SQL-Parser (greenlion fork) |
| offsite-solutions/eisodos-sqlparser | 181 | excluded | — |
| codexsoft/sql-parser | 46 | excluded | — |
| subapp/sql | 19 | unresolved_blocked | subapp/sql lexer and parser |
| xp-forge/sql-parser | 4 | excluded | xp-forge Pratt parser |
| cadfael/mysql-antlr4-parser | 2 | excluded | ANTLR MySQL grammar |
| inilim/sqlite-parser | 1 | unresolved | inilim/sqlite-parser phplrt grammar (typed SQLite AST) |
| k-kinzal/sql-parser | 0 | excluded | — |

Reasons are in [leads.json](leads.json). Standard and runtime findings are in [standard.json](standard.json).
