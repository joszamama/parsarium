# YAML / PHP — pilot

**Status:** pilot_one_verified_bounded_search; incomplete. 1 verified third-party paths, 0 verified standard APIs, 1 verified Docker harnesses.

One verified PHP YAML path. symfony/yaml v8.1.11 parses both schema-neutral valid controls through the documented Yaml::parse(string) with Yaml::PARSE_OBJECT_FOR_MAP into exact ordered typed trees; without that flag mappings become PHP arrays and {} cannot be told from []. Xdebug covers 570 package lines (365 in Parser.php); the parser-line AFL++ bridge repeats identically three times per control and the controls differ by 61 lines and 61 tuples, all in Parser.php, Inline.php and Unescaper.php. mustangostang/spyc 0.6.3 is excluded: it leaves \u and \t escapes undecoded, drops the final line break of clip-chomped block scalars, misreads '|-' with more-indented lines and returns '...' as a sequence item. dallgoot/yaml 1.0.1 (372,583) is excluded: it leaves \" and \t escapes and the single-quoted '' escape undecoded. The PECL yaml extension (libyaml family; no Packagist metric) remains an unverified lead. The bounded Packagist search used one query ('yaml', first 100 of 1,954 hits). Packagist downloads are package adoption, mostly transitive through Symfony and Laravel, not YAML parsing frequency. Two valid controls do not establish tags, merge keys, multi-document streams, YAML 1.1-only scalars or malformed-input behavior.

[Ranking and search limits](../../../data/php/yaml/ranking.md) · [Standard API inventory](../../../data/php/yaml/standard.json)

## Third-party parsers

- [symfony/yaml](symfony-yaml/README.md) — verified Docker harness
- [pecl/yaml](pecl-yaml/README.md) — verified API path

## Standard and runtime APIs

None verified in this pilot cell yet.
