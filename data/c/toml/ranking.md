# C × TOML: selected parsers

0 selected third-party paths; bounded pilot scope.

## Primary within-cell adoption metric

Debian popcon installations ([registry-snapshot.json](registry-snapshot.json), captured 2026-11-17). No C TOML library is packaged in Debian or Conan Center, so no C path has the primary metric or a Debian fallback of at least 1,000. GitHub stars are a fallback only in PLY cells.

tomlc17 R261116 and toml-c (commit 6a38d404, tomlc99 family) passed both controls, coverage and AFL++ feedback; they are recorded as `unresolved_no_primary_metric` leads with that evidence in [leads.json](leads.json). tomlc99 fails the second control; libtoml (TOML 0.4.0) was not run.

## Standard library

None documented; see [standard.json](standard.json).
