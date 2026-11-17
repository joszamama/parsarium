# PHP × TOML: selected parsers (pilot)

2 control-verified third-party paths selected. The ceiling is ten; this pilot does not pad the selection. A path is an API or package route, not necessarily an independent parser engine. PHP has no standard-library TOML API ([standard.json](standard.json)).

## Primary within-cell adoption metric

Packagist total downloads, from the bounded search captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [internal/toml](https://packagist.org/packages/internal/toml) | 1.1.3 | 325,891 | One TOML document via `Toml::parse(string)`; Document AST walked into the typed tree and checked against `Document::toArray()` | internal/toml Lexer, recursive-descent Parser and AST |
| 2 | [php-collective/toml](https://packagist.org/packages/php-collective/toml) | 0.1.5 | 28,378 | One TOML document via `Toml::tryParse(string)` (same Parser and Normalizer as `decode()`); AST walked into the typed tree and checked against the normalized array | php-collective/toml Lexer, Parser, AST and Normalizer |

The two paths share no parser code. Neither array API keeps every TOML scalar kind: internal/toml's `parseToArray()` returns local date-times and local dates as `DateTimeImmutable` values, just like offset date-times, and local times as strings, and php-collective/toml's `decode()` returns all three local kinds as strings. Each harness therefore reads the kinds from the library's documented AST value nodes, places them where the library's own array assembly places their values, and requires the two to agree. Both valid controls ([service-config](../../../controls/toml/service-config.toml), [typed-scalars](../../../controls/toml/typed-scalars.toml)) match the hand-written typed trees exactly.

internal/toml: Xdebug covers 547 package lines on service-config and 608 on typed-scalars. The parser-line AFL++ bridge repeats identically three times on each control and differs by 255 lines and 255 tuples between them, mostly in `Lexer.php` and `Parser.php` ([receipt](internal-toml-feedback-differential.json)). php-collective/toml: Xdebug covers 825 and 780 package lines; the bridge differs by 477 lines and 475 tuples, in `Lexer.php`, `Parser.php`, `Normalizer.php` and the AST value classes ([receipt](php-collective-toml-feedback-differential.json)).

Unverified leads ([leads.json](leads.json)): [yosymfony/toml](https://packagist.org/packages/yosymfony/toml) v1.0.4 (1,996,947 downloads) implements TOML 0.4.0, and its `Toml::parse` rejects typed-scalars with `Syntax error: unexpected token "T_UNQUOTED_KEY" at line 6 with value "xDEAD_BEEF"`, because that TOML version has no hexadecimal integers. [devium/toml](https://packagist.org/packages/devium/toml) 1.1.1 (134,459) matches service-config, but it returns typed-scalars' local time `00:32:00.25` as `TomlLocalTime` with `millisecond: 25`, which is 0.025 s. Eleven leads with lower download counts or old-draft parsers have not been run: jamesmoss/toml (31,882), leonelquinteros/php-toml (7,863), zidizei/toml-php (121), app-hive/toml (30), petalbranch/toml (20), checkdomain/php-toml (15), dayvsonspacca/psl-toml (4), makhnanov/toml (3, a yosymfony fork), azjezz/toml (1), cline/toml (0, a yosymfony fork) and blixon/toml (0).
