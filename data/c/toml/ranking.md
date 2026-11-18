# C × TOML: selected parsers

1 selected third-party path; bounded pilot scope.

## Primary within-cell adoption metric

Debian popcon installations ([registry-snapshot.json](registry-snapshot.json), captured 2026-11-17). No C TOML library is packaged in Debian or Conan Center, so no C path has the primary metric or a Debian fallback of at least 1,000.

## GitHub-star fallback (secondary)

Since 2026-11-18, C and C++ cells may fill slots left empty after primary and Debian paths with pinned tagged releases of format-specific upstream repositories that have at least 100 GitHub stars ([PROTOCOL.md](../../../PROTOCOL.md)). Stars measure repository interest, not downloads or installations; they are ranked separately and are not comparable with popcon values. The counts come from the GitHub repos API, captured 2026-11-18 with response hashes in the snapshot's `round_6_star_fallback` record.

| Rank | Package | Release | GitHub stars (star fallback) | Parsed scope | Parser family |
| --- | --- | --- | --- | --- | --- |
| 1 | [tomlc17](https://github.com/cktan/tomlc17/blob/R261116/API.md#toml_parse) | R261116 | 201 GitHub stars (secondary, repository interest, not downloads; popcon: not packaged) | TOML 1.0.0 byte buffer via `toml_parse(src, len)` into a `toml_datum_t` tree | tomlc17 (own single-file `src/tomlc17.c`) |

tomlc17 R261116 is pinned from its [release tag](https://github.com/cktan/tomlc17/releases/tag/R261116) archive, SHA-256 `0a9fd8636cf79a08a01e75cb04a1a62b7e0e689576c2407cc1d571e92df7df4b` (MIT). R261116 is the latest release. The harness calls the [documented](https://github.com/cktan/tomlc17/blob/R261116/API.md#toml_parse) `toml_parse(src, len)` on the exact bytes and walks the returned `toml_datum_t` tree; offset date-times become UTC instants from the datum's date, time, microsecond and `tz` minute fields, and the four date-time kinds keep their own types. Both controls equal their expected typed trees. The base control covers 1,034 lines of `src/tomlc17.c`. The parser-only probe instruments only `tomlc17.c` (checked with `nm`); three runs per control repeat exactly, and the controls differ by 216 of 268/368 AFL++ tuples and 424 source lines ([receipt](../../../fuzzing/afl-native/toml/c/tomlc17/differential.json)). It is a separate rewrite by the tomlc99 author and shares no parser code with tomlc99.

## Leads that do not qualify

- toml-c (114 stars, tomlc99 family fork) passed both controls, coverage and AFL++ feedback at commit `6a38d404`, but the repository has no tagged release, so the star fallback does not apply.
- tomlc99 (664 stars) has no tagged release and its latest commit rejects the second control (`expect hex char` on a lowercase `\u` escape).
- libtoml (125 stars) has no tagged release and targets TOML 0.4.0; it was not run.
- fwm (187 stars) is a Wayland compositor, not a TOML library.

Details are in [leads.json](leads.json).

## Standard library

None documented; see [standard.json](standard.json).
