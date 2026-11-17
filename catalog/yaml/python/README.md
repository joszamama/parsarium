# YAML / Python — pilot

**Status:** pilot_six_verified_bounded_search; incomplete. 6 verified third-party paths, 0 verified standard APIs, 6 verified Docker harnesses.

Six verified third-party paths in PyPI last_month order: PyYAML 6.0.3 (1,227,712,536); PyYAML CSafeLoader (libyaml) 6.0.3 (1,227,712,536); ruamel.yaml 0.19.1 (177,667,165); ruamel.yaml.clib 0.2.15 (69,289,256); srsly 3.0.1 (24,260,205); yamlcore 0.1.1 (92,413). PyYAML (pure SafeLoader) and ruamel.yaml (YAML(typ='safe', pure=True)) are pure-Python loaders with Python line coverage of their own package. PyYAML CSafeLoader is a separate route of the same PyPI package (its metric is the PyYAML package value, not a split) whose scanner/parser is libyaml 0.2.5, built from source with LLVM coverage and linked statically into _yaml. ruamel.yaml.clib is ruamel.yaml's C loader package with its own metric; its vendored C is an older libyaml snapshot (96.1% of distinct lines shared with libyaml 0.2.5), so it shares the libyaml family with the CSafeLoader path. srsly.yaml_loads is a labelled wrapper over the same pure ruamel.yaml route; its own lines are identical on both controls. yamlcore.CoreLoader is a labelled wrapper over PyYAML's pure BaseLoader with its own YAML 1.2 core resolver/constructors. Native routes report LLVM regions of the parser C; Python routes report executed lines; each has three identical AFL++ runs per control that differ in scanner/parser sources. The bounded search (project name contains 'yaml'; first 100 alphabetical hits of 798, captured 2026-11-17) and named leads are recorded; remaining leads are in leads.json. A supplementary check of 13 named high-adoption PyPI projects outside that window (C routes, wrappers, forks, loader plugins; 2026-11-17) is recorded in registry-snapshot.json; strictyaml fails both controls, oyaml/yamlloader/yamlordereddictloader/pydantic-yaml are excluded as re-export or mapping layers, PyYAML-ft and ruyaml as identical or predecessor forks, and rapidyaml and yaml-rs remain unresolved native leads. Package adoption is not YAML-specific use. The two controls cover a schema-neutral YAML 1.2 subset only, not tags, merge keys, multi-document streams, complex keys, YAML 1.1-only scalars or malformed input.

[Ranking and search limits](../../../data/python/yaml/ranking.md) · [Standard API inventory](../../../data/python/yaml/standard.json)

## Third-party parsers

- [PyYAML](pyyaml/README.md) — verified Docker harness
- [PyYAML CSafeLoader (libyaml)](pyyaml-csafeloader-libyaml/README.md) — verified Docker harness
- [ruamel.yaml](ruamel-yaml/README.md) — verified Docker harness
- [ruamel.yaml.clib](ruamel-yaml-clib/README.md) — verified Docker harness
- [srsly](srsly/README.md) — verified Docker harness
- [yamlcore](yamlcore/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
