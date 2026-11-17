# PHP × YAML: selected parsers (pilot)

Two control-verified third-party paths are selected. The ceiling is ten; the cell is not padded.

## Primary within-cell adoption metric

Packagist lifetime downloads, captured 2026-11-17 ([snapshot](registry-snapshot.json)). Values are package adoption, mostly transitive, not YAML-specific use, and are compared only within this cell. pecl/yaml is a php-ext (PIE) package: its count covers installs through Packagist only, not PECL or distribution packages.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [symfony/yaml](https://symfony.com/doc/8.1/components/yaml.html) | v8.1.11 | 926,050,815 | One YAML document via `Yaml::parse(string, Yaml::PARSE_OBJECT_FOR_MAP)` into an exact ordered typed tree | Symfony Yaml own Parser/Inline/Unescaper |
| 2 | [pecl/yaml](https://www.php.net/manual/en/function.yaml-parse.php) | 2.3.0 | 55,298 | One YAML document via `yaml_parse(string)` with a `YAML_MAP_TAG` callback into an exact ordered typed tree | libyaml via the PECL yaml C extension |

## Leads (unverified or excluded)

| Lead | Status | Metric | Parser family |
| --- | --- | ---: | --- |
| mustangostang/spyc | excluded | 51,101,645 | Spyc |
| dallgoot/yaml | excluded | 372,583 | dallgoot/yaml |

mustangostang/spyc fails both valid controls ([probe](spyc-valid-control-probe.json)); dallgoot/yaml fails the primary control ([probe](dallgoot-yaml-valid-control-probe.json)). Standard and runtime APIs: none documented ([standard.json](standard.json)).
