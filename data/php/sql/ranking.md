# PHP × SQL: pilot ranking

Four third-party paths are control verified against the hand-written oracle in [controls/sql/expected.json](../../../controls/sql/expected.json), with a pinned Docker harness, parser-source coverage and stable AFL++ feedback that differs between the two controls. Paths are ranked only among verified paths in this cell. The ceiling is ten, and the cell is not padded. The scope, controls and oracle are in [catalog/sql/PROTOCOL.md](../../../catalog/sql/PROTOCOL.md).

## Primary within-cell adoption metric

Packagist total downloads, captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [phpmyadmin/sql-parser](https://github.com/phpmyadmin/sql-parser/blob/6.0.1/README.md#parsing) | 6.0.1 | 55,800,144 | `new PhpMyAdmin\SqlParser\Parser(local SQL text, strict: true) -> statements[]`; dialect: MySQL (library default context) | phpMyAdmin sql-parser hand-written lexer and statement parser |
| 2 | [greenlion/php-sql-parser](https://github.com/greenlion/PHP-SQL-Parser/blob/7a4701b71f7786e8518a9412f3c552ae4550d314/README.md) | v5.0.0 | 13,810,212 | `(new PHPSQLParser\PHPSQLParser())->parse(local SQL text) -> clause-keyed array parse tree`; dialect: MySQL-oriented (no dialect option) | PHP-SQL-Parser lexer and clause processors (nested array parse tree) |
| 3 | [soundintheory/php-sql-parser](https://github.com/soundintheory/php-sql-parser/blob/dcb81216a13be124d21711b8fefb6e80db7af472/README.md) | 1.0 | 599,598 | `(new PHPSQL\Parser())->parse(local SQL text) -> clause-keyed array parse tree`; dialect: MySQL-oriented (no dialect option) | PHP-SQL-Parser lineage (2013 PSR-0 fork of the Google Code php-sql-parser; shared family with greenlion/php-sql-parser) |
| 4 | [sad_spirit/pg_builder](https://github.com/sad-spirit/pg-builder/blob/2a1ff9bf16b014f37af1fce1c4b9db53782fe7f6/README.md) | v3.3.1 | 76,924 | `(new sad_spirit\pg_builder\StatementFactory())->createFromString(local SQL text) -> Statement AST`; dialect: PostgreSQL (the only dialect; default Lexer options) | pg_builder hand-written PostgreSQL lexer and recursive-descent parser (typed AST) |

Receipts: [phpmyadmin/sql-parser](../../../projects/sql/php/phpmyadmin_sql_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/php/phpmyadmin_sql_parser/differential.json), [greenlion/php-sql-parser](../../../projects/sql/php/greenlion_php_sql_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/php/greenlion_php_sql_parser/differential.json), [soundintheory/php-sql-parser](../../../projects/sql/php/soundintheory_php_sql_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/php/soundintheory_php_sql_parser/differential.json), [sad_spirit/pg_builder](../../../projects/sql/php/sad_spirit_pg_builder/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/php/sad_spirit_pg_builder/differential.json).

## Leads by the same metric

| Lead | Metric | Status | Parser family |
| --- | ---: | --- | --- |
| doctrine/sql-formatter | 216,519,891 | excluded | — |
| jdorn/sql-formatter | 120,134,108 | excluded | — |
| iamcal/sql-parser | 72,745,721 | excluded | iamcal/sql-parser |
| phpmyadmin/sql-parser | 55,800,144 | selected | phpMyAdmin hand-written lexer and parser |
| greenlion/php-sql-parser | 13,810,212 | selected | PHP-SQL-Parser |
| soundintheory/php-sql-parser | 599,598 | selected | PHP-SQL-Parser lineage (2013 fork; shared with greenlion) |
| sqlftw/sqlftw | 169,733 | unresolved | SQLFTW |
| sad_spirit/pg_builder | 76,924 | selected | pg_builder hand-written PostgreSQL parser |

Reasons are in [leads.json](leads.json). Standard and runtime findings are in [standard.json](standard.json).
