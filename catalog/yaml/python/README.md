# YAML / Python — pilot

**Status:** pilot_one_verified_bounded_search; incomplete. 1 verified third-party paths, 0 verified standard APIs, 1 verified Docker harnesses.

One verified third-party path, in PyPI last_month order: PyYAML 6.0.3 through the pure-Python yaml.SafeLoader (1,227,712,536 last-month downloads; YAML 1.1 resolvers; the libyaml CSafeLoader route is a separate unresolved lead). Each gives the hand-written typed tree on both schema-neutral YAML controls through bytes, decoded str and a local binary stream, with Python line coverage of its own package and three identical AFL++ line-bridge runs per control whose controls differ in scanner.py and parser.py lines. The bounded search (project name contains 'yaml'; first 100 alphabetical hits of 798, captured 2026-11-17) and named leads are recorded; remaining leads (strictyaml and oyaml/yamlcore as wrappers, rapidyaml, and PyYAML's CSafeLoader route) are unverified. Package adoption is not YAML-specific use. The two controls cover a schema-neutral YAML 1.2 subset only, not tags, merge keys, multi-document streams, complex keys, YAML 1.1-only scalars or malformed input.

[Ranking and search limits](../../../data/python/yaml/ranking.md) · [Standard API inventory](../../../data/python/yaml/standard.json)

## Third-party parsers

- [PyYAML](pyyaml/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
