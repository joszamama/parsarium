# YAML cell protocol

This cell applies the [general protocol](../../PROTOCOL.md) to YAML 1.2 documents read as local UTF-8 text, one document per control. JSON is a separate cell even though it is close to a YAML 1.2 subset.

## Eligibility

A path qualifies only if it parses YAML text from local bytes, a string, a file or a stream and returns the document it parsed: a node tree, native values, or an event stream that the harness assembles. Emitters and serializers, schema validators without their own parse step, YAML-front-matter splitters, CLI-only tools and remote services are excluded. A wrapper qualifies as a package API with its underlying parser family stated, for example `sigs.k8s.io/yaml` over a go-yaml fork, `jackson-dataformat-yaml` over SnakeYAML, `strictyaml` over ruamel.yaml, or PHP ext-yaml (PECL) over libyaml. Python PyYAML's pure-Python `SafeLoader` and its libyaml-backed `CSafeLoader` are separate paths with separate families, and each project states which one it runs.

Under the concrete-syntax-tree rule in the [general protocol](../../PROTOCOL.md), C tree-sitter-yaml stays excluded. Its tree keeps escapes, block scalars and aliases as written, so the harness would have to decode, fold, chomp and expand them itself. Typing plain scalars from their text, as the libyaml and libfyaml adapters do, would be allowed.

The harness reports the whole document as a typed tree in source order: `["map", [[key, node], ...]]`, `["seq", [node, ...]]`, `["str", text]`, `["int", decimal]`, `["float", shortest round-trip decimal]`, `["bool", true|false]` and `["null"]`. Aliases are expanded to their anchored node. Where an API returns native values that do not keep the int/float distinction (JavaScript numbers), the harness types a finite integral number as `int`; the controls contain no integral-valued floats, so this is recorded but cannot change the result.

## Controls

- `controls/yaml/catalog.yaml`: the primary control, 483 bytes. A block-mapping root with a comment, ints, floats, `true`/`false`, `null`, a double-quoted string with `é`, `\"` and `\t` escapes, a single-quoted string with `''`, a flow sequence and a flow mapping, a block sequence of mappings, literal (`|`) and folded (`>`) block scalars, non-ASCII plain text, and an anchor (`&base`) with one alias (`*base`).
- `controls/yaml/order.yaml`: the fixed second control for AFL++ feedback, 345 bytes. A block-sequence root between `---` and `...` markers, nested block sequences, empty flow collections, an anchored mapping repeated by alias, nested flow collections, a multi-word plain scalar, a `\n` escape, a strip-chomped literal block with more-indented lines, `~` and `false`.

Both are UTF-8 without a BOM, tabs (outside the `\t` escape), carriage returns, directives, tags, merge keys, complex keys or duplicate keys. **Scalar restriction:** every plain scalar types the same under YAML 1.1 resolvers (PyYAML, libyaml loaders, SnakeYAML, go-yaml v2) and the YAML 1.2 core schema. The controls avoid `yes`/`no`/`on`/`off`/`y`/`n`, leading-zero, octal, hexadecimal and binary integers, sexagesimal numbers, exponents without a dot, timestamps and `<<`; a string that would resolve otherwise (the ZIP code `"10115"`) is quoted. Libraries on either schema must therefore agree. The controls do not test tags, merge keys, multi-document streams, YAML 1.1-only scalars, comments as data or malformed input.

`controls/yaml/check_controls.py` is the oracle. It holds a hand-written expected typed tree for each control, pins the control hashes, checks the scalar restriction against the source, and cross-checks both trees with Ruby Psych `safe_load` (Psych 3.1.0 over libyaml 0.2.1 on the capture host). Psych is outside the eight ecosystems but shares the libyaml family with C libyaml, PyYAML's CLoader and PHP ext-yaml, so for those paths the hand-written tree is the independent reference.

## Adoption

Paths are ranked within one ecosystem by the primary metric its JSON and XML cells use: Debian popcon `sourcemax` installations for C and C++, pkg.go.dev Imported by for Go, deps.dev `directDependentCount` summed over Maven releases for Java, npm last-month downloads for JavaScript, PyPI Stats `last_month` for Python, crates.io 90-day `recent_downloads` for Rust, and Packagist lifetime downloads for PHP. `scripts/capture_yaml_registry.py` records each bounded search (query `yaml`, first 100 hits) and one value per lead in `data/<ecosystem>/yaml/registry-snapshot.json`. Wrappers and forks keep their own metric and are marked as a shared family. The ceiling is ten paths, and the cell is not padded.

## Standard and runtime APIs

None of the eight scoped standard libraries or runtimes documents a YAML parser; each cell's `standard.json` cites the documentation checked. PHP's `yaml_parse` is a PECL extension, not a bundled one, and is a third-party lead.

## AFL++

The overlay must show parser-derived feedback on both controls. Each control runs three times under `afl-showmap`; the receipt records the edge or feature counts, that repeats are identical, the edges unique to each control, and per-file parser source lines. The overlay checks only launchers and feedback. It runs no campaign and tests no malformed inputs.

## Fandango

[Fanbase](https://github.com/fandango-fuzzer/fanbase) has no YAML spec (its `specs/` index lists 33 formats, none YAML, as of 2026-11-17). The bundled [`yaml.fan`](../../fuzzing/fandango/specs/yaml.fan) generates small block-mapping documents within the same schema-neutral scalar restriction; quoted strings deliberately carry `yes`, `on`, `0755`, `1:30` and `10115` so a resolver must keep them strings. Twenty outputs from Fandango 1.3.1 (`-n 20 --random-seed 1`, `PYTHONHASHSEED=1`) all loaded with Psych `safe_load`.
