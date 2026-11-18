# TOML cell protocol

This cell applies the [general protocol](../../PROTOCOL.md) to TOML 1.0.0 documents encoded in UTF-8 and read as local text. TOML is a pilot format: its eight cells stay incomplete, and its counts never enter the ten active-format totals.

## Eligibility

A path qualifies only if it reads TOML text from a local file, byte buffer, stream, or in-memory string and returns what it parsed. The package API itself has to tokenize and parse the document. Serializers and writers (for example `tomli-w`), schema validators, formatters and linters without a documented value or syntax-tree API, configuration loaders that only delegate to a selected parser, and CLIs are excluded or left as leads in `data/<ecosystem>/toml/leads.json`. A typed mapping library counts only when it exposes a documented generic value view (a table/value tree, a dynamic map, or a syntax tree with typed values).

A syntax tree counts only under the concrete-syntax-tree rule in the [general protocol](../../PROTOCOL.md). A grammar whose tree leaves dotted keys and table headers unmerged, or strings undecoded, does not qualify, because the harness would build the TOML table tree itself. Debian packages no tree-sitter TOML grammar.

A wrapper over another selected parser can be its own package path, but its family is recorded. An empty compatibility distribution that only installs another parser is not a separate path. Standard and runtime APIs are recorded separately in `standard.json`. Python's `tomllib` (3.11+) is a standard API path, not a third-party one; it is a vendored copy of `tomli`, so the two share one family.

## Observed result: the typed tree

Each harness reports the whole document as a typed tree modeled on the [toml-test](https://github.com/toml-lang/toml-test) JSON encoding:

- a table is a JSON object and an array is a JSON array; key order is not significant;
- every scalar is `{"type": T, "value": S}` where `S` is a string;
- `string`: the decoded string;
- `integer`: decimal digits with an optional leading `-` (hexadecimal, octal, binary and underscores are normalized);
- `float`: the shortest round-trip decimal digits written positionally with at least one fractional digit (`1e3` → `1000.0`, `1.5625e-2` → `0.015625`);
- `bool`: `true` or `false`;
- `datetime` (offset date-time): the UTC instant `YYYY-MM-DDTHH:MM:SS[.fraction]Z`;
- `datetime-local`, `date-local` and `time-local`: `YYYY-MM-DDTHH:MM:SS[.fraction]`, `YYYY-MM-DD` and `HH:MM:SS[.fraction]`.

A fraction keeps only its significant digits and is omitted when zero. Normalizing offset date-times to the UTC instant matches toml-test's instant comparison and keeps the tree comparable across APIs that return an instant rather than the written offset. A harness that has to rebuild a scalar from a library's own representation (for example a JavaScript `Date` or a Java `OffsetDateTime`) formats it with these rules; it never re-parses the input text itself.

## Controls

- [`controls/toml/service-config.toml`](../../controls/toml/service-config.toml): the primary control, 517 bytes. Root keys before the first table, nested `[servers.alpha]`/`[servers.beta]` tables, an inline table, an array of inline tables, a two-element array of tables, a basic string with `\"` escapes, non-ASCII text, integers, a float, booleans and a UTC offset date-time.
- [`controls/toml/typed-scalars.toml`](../../controls/toml/typed-scalars.toml): the fixed second control for AFL++ feedback, 616 bytes. Signed, underscored, hexadecimal, octal and binary integers; fractional and exponent floats; basic, literal, multi-line basic (with a line-ending backslash) and multi-line literal strings with `\t`, `\"`, `\\` and `é` escapes; an offset date-time with fractional seconds and a `-07:00` offset; local date-time, local date and local time; quoted and dotted keys.

Both files are UTF-8 with LF line endings, contain no tabs, NaN, infinity, heterogeneous arrays or integers above 2^53, and are valid TOML 1.0.0. The expected trees, [`service-config.expected.json`](../../controls/toml/service-config.expected.json) and [`typed-scalars.expected.json`](../../controls/toml/typed-scalars.expected.json), were written by hand from the TOML 1.0.0 specification. [`check_controls.py`](../../controls/toml/check_controls.py) pins both control hashes, parses each control with Python's standard-library `tomllib`, builds the typed tree and requires equality with the committed file. `tomllib` is the oracle; for the Python `tomli` path, which shares its code, the hand-written tree is the independent check.

A path may verify only a subset when its API cannot represent part of a control (for example, a library that drops the offset of an offset date-time and keeps only a local time). Such a path stays a lead unless the subset is stated in its record and both controls still match on that subset; it is never silently adjusted.

## Adoption

Paths are ranked within one ecosystem by the primary metric its JSON and XML pilot cells use:

| Ecosystem | Primary metric |
| --- | --- |
| C | Debian popcon installations; no C TOML library is packaged in Debian or Conan Center, so no C path has the primary metric or a Debian fallback of at least 1,000. Paths without either may fill the remaining slots with GitHub stars of at least 100 (PROTOCOL.md star fallback, 2026-11-18), ranked separately |
| C++ | Debian popcon installations (source-package `sourcemax/by_inst`, binary package recorded beside it) |
| Go | pkg.go.dev "Imported by" count |
| Java | deps.dev `directDependentCount` summed over all Maven releases |
| JavaScript | npm downloads over the last month |
| Python | PyPI Stats `last_month` downloads, mirrors excluded |
| Rust | crates.io 90-day recent downloads from the search API |
| PHP | Packagist lifetime downloads |

Bounded searches are captured by [`scripts/snapshot_toml_registry.py`](../../scripts/snapshot_toml_registry.py) into `data/<ecosystem>/toml/registry-snapshot.json`: each query keeps at most the first 100 hits, with its URL, date and total. The ceiling is ten paths, and the cell is not padded.

## AFL++

The overlay must show parser-derived feedback on both controls. Each control runs at least three times under the ecosystem's AFL++ route, and the receipt records the edge or tuple counts, that repeats are identical, the edges unique to each control, and per-file parser source lines. The overlay checks only launchers and feedback. It runs no campaign and tests no malformed inputs.

## Fandango

Fanbase (index schema 2, commit `d20f8d05`, 2026-11-16) ships no TOML spec. The local [`toml.fan`](../../fuzzing/fandango/specs/toml.fan) generates small valid TOML 1.0.0 seeds: fixed key names per position (so no key or table is redefined), optional `[server]`, `[owner]` and dotted-key tables, zero to three `[[products]]` tables, and typed scalars of every kind. With Fandango 1.3.1, `--random-seed 1`, `PYTHONHASHSEED=0` and `-n 200`, all 200 outputs were distinct and `tomllib` parsed every one.
