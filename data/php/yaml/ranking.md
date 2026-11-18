# PHP × YAML: selected parsers (pilot)

Three control-verified third-party paths are selected. The ceiling is ten; the cell is not padded.

## Primary within-cell adoption metric

Packagist lifetime downloads, captured 2026-11-17 (purrphp/yaml: round-4 targeted lookup, 2026-11-18) ([snapshot](registry-snapshot.json)). Values are package adoption, mostly transitive, not YAML-specific use, and are compared only within this cell. pecl/yaml is a php-ext (PIE) package: its count covers installs through Packagist only, not PECL or distribution packages.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [symfony/yaml](https://symfony.com/doc/8.1/components/yaml.html) | v8.1.11 | 926,050,815 | One YAML document via `Yaml::parse(string, Yaml::PARSE_OBJECT_FOR_MAP)` into an exact ordered typed tree | Symfony Yaml own Parser/Inline/Unescaper |
| 2 | [pecl/yaml](https://www.php.net/manual/en/function.yaml-parse.php) | 2.3.0 | 55,298 | One YAML document via `yaml_parse(string)` with a `YAML_MAP_TAG` callback into an exact ordered typed tree | libyaml via the PECL yaml C extension |
| 3 | [purrphp/yaml](https://github.com/PurrPHP/yaml/blob/c069a72e06e5a11a725b50226122f1eb26eb64fe/README.md) | 1.0.0 | 1,088 | One YAML document via `YamlStreamSingle::fromString(string)`; node model walked in source order, scalars typed by the package's `CoreSchema::resolve` | PurrPHP Yaml own line reader, Parser/InlineParser and CoreSchema |

## Leads (unverified or excluded)

| Lead | Status | Metric | Parser family |
| --- | --- | ---: | --- |
| nette/neon | excluded | 73,698,888 | NEON (Nette Object Notation), a YAML-like format |
| mustangostang/spyc | excluded | 51,101,645 | Spyc |
| grasmash/yaml-expander | excluded | 32,985,782 | symfony/yaml (Yaml::parse into PHP arrays) plus placeholder expansion |
| grasmash/yaml-cli | excluded | 31,791,136 | symfony/yaml via a Symfony Console CLI |
| wp-cli/mustangostang-spyc | excluded | 22,190,290 | Spyc (WP-CLI fork of mustangostang/spyc) |
| hassankhan/config | excluded | 14,263,728 | symfony/yaml (Yaml::parse with PARSE_CONSTANT into PHP arrays) |
| pragmarx/yaml | excluded | 2,958,371 | symfony/yaml or ext-yaml via a Laravel config loader |
| jbzoo/data | excluded | 1,679,280 | symfony/yaml (Yaml::parse into PHP arrays) |
| aplus/config | excluded | 1,609,834 | libyaml via ext-yaml (yaml_parse_file) |
| dallgoot/yaml | excluded | 372,583 | dallgoot/yaml |
| maikuolan/common | excluded | 251,761 | Maikuolan Common YAML handler (own line parser) |
| webignition/yaml-document-set-parser | excluded | 84,925 | document splitter (no YAML parser) |
| xp-forge/yaml | excluded | 36,737 | xp-forge/yaml (own parser) |
| horde/yaml | excluded | 12,259 | Horde_Yaml (own loader) |
| mougrim/yaml-cst | excluded | 8,374 | tree-sitter-yaml via FFI |
| eureka/component-yaml | excluded | 3,704 | Spyc 0.5.1 (renamed copy) |
| secondparty/dipper | excluded | 2,553 | Dipper (own subset parser) |
| yalesov/yaml | excluded | 1,694 | symfony/yaml (Yaml::parse into PHP arrays) |
| charcoal-dev/yaml | excluded | 1,640 | comely-io/yaml lineage (own line parser) |
| klausi/yaml_comments | excluded | 1,482 | Symfony Yaml fork (comment-preserving) |
| comely-io/yaml | excluded | 1,445 | comely-io/yaml (own line parser) |
| sndsgd/yaml | excluded | 1,298 | libyaml via ext-yaml (pecl/yaml family) |
| pieter/yaml | excluded | 1,276 | symfony/yaml 2.5.5 via a Laravel 4 loader |
| phpalchemy/yaml | excluded | 980 | Spyc-derived ("maintained version of spyc") |
| mecha-cms/x.y-a-m-l | excluded | 562 | mecha-cms/x.y-a-m-l |
| 3rd-party/yaml | excluded | 406 | Spyc-derived (phpalchemy/yaml variant) |
| aeliot/yaml-token | excluded | 352 | yaml-token own lexer and node/token tree |
| maxbeckers/php-yaml-parser | excluded | 309 | maxbeckers/php-yaml-parser (own scan parser) |
| atphp/yaml | excluded | 257 | wrapper over several YAML parsers |
| gijsbos/yamlspeed | excluded | 132 | YamlSpeed (own parser) |
| rindow/rindow-module-yaml | excluded | 78 | symfony/yaml via a Rindow module |
| nigatedev/yaml | excluded | 28 | symfony/yaml v5.3.6 |
| taufik-nurrohman/y-a-m-l | excluded | 27 | y-a-m-l own pure-PHP converter (Mecha CMS) |
| tbela99/yaml | excluded | 15 | symfony/yaml 5.1 fork (comment-preserving AST) |
| keruald/yaml | excluded | 13 | symfony/yaml |
| scottchiefbaker/yaml-polyfill | excluded | 8 | yaml-polyfill (own pure-PHP yaml_parse) |

mustangostang/spyc fails both valid controls ([probe](spyc-valid-control-probe.json)); dallgoot/yaml fails the primary control ([probe](dallgoot-yaml-valid-control-probe.json)). The round-2 leads were probed on both valid controls or excluded from source evidence ([probes and reasons](round2-lead-probes.json), [leads](leads.json)): wrappers over symfony/yaml return PHP arrays that lose {} versus [], nette/neon is NEON, the own parsers and Spyc forks fail escapes, aliases or block scalars, and tbela99/yaml is a symfony/yaml 5.1 fork. Searches: `yaml`, `yaml parser`, `yaml-parser`, `yml`, `spyc` (first 100 hits each). Standard and runtime APIs: none documented ([standard.json](standard.json)). Round 4 (2026-11-18) added purrphp/yaml from a GitHub search for PHP YAML parsers and decided the other round-4 leads ([probes](round4-lead-probes.json)).
