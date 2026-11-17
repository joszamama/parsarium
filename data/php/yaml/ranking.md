# PHP × YAML: selected parsers (pilot)

One control-verified third-party path is selected. The ceiling is ten; the cell is not padded.

## Primary within-cell adoption metric

Packagist lifetime downloads, captured 2026-11-17 ([snapshot](registry-snapshot.json)). Values are package adoption, mostly transitive, not YAML-specific use, and are compared only within this cell.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [symfony/yaml](https://symfony.com/doc/8.1/components/yaml.html) | v8.1.11 | 926,050,815 | One YAML document via `Yaml::parse(string, Yaml::PARSE_OBJECT_FOR_MAP)` into an exact ordered typed tree | Symfony Yaml own Parser/Inline/Unescaper |

## Leads (unverified or excluded)

| Lead | Status | Metric | Parser family |
| --- | --- | ---: | --- |
| mustangostang/spyc | excluded | 51,101,645 | Spyc |
| dallgoot/yaml | unresolved | 372,583 | dallgoot/yaml |
| pecl/yaml | unresolved | n/a | libyaml via PECL ext-yaml |

mustangostang/spyc fails both valid controls ([probe](spyc-valid-control-probe.json)). Standard and runtime APIs: none documented ([standard.json](standard.json)).
