# Working in this repository

Guidance for automated agents and new contributors. Read [README.md](README.md) for what Parsarium is, [PROTOCOL.md](PROTOCOL.md) for the selection rules, and [ETHICS.md](ETHICS.md) for the limits on what the repository is used for.

## Map

| Path | Contents |
| --- | --- |
| `parsarium.py` | Repository CLI: `list`, `catalog`, `projects`, `show`, `build`, `run`, `run-format`, `replay`, `afl`, `native`, `fandango`, `report` |
| `src/parsarium/` | Installable package (`parsarium` command, `run-selection`, snapshot handling) |
| `data/formats.json` | Format registry: active and pilot formats, read by scripts and the website |
| `data/<ecosystem>/<format>/` | One cell: `cell.json` (status, counts, search limits, uncertainty), `parsers.json` (selected third-party paths), `standard.json`, `leads.json` (candidates not counted, with reasons), `ranking.md`, `registry-snapshot.json` (hashed adoption-metric captures), receipts |
| `data/curation/` | Ten-path selection plan, metric snapshots (Debian popcon, GitHub stars), exclusions, displacement and merge records |
| `data/cells.json`, `data/pilot-cells.json`, `data/projects-coverage.json`, `data/*-smoke.json` | Aggregates. Generated; never edit by hand |
| `catalog/<format>/` | Format protocols (`PROTOCOL.md` where a format has extra rules) and generated READMEs |
| `controls/<format>/` | Small valid inputs and the generators or oracles that check them |
| `projects/<format>/<ecosystem>/<slug>/` | One runnable target: `manifest.json`, `Dockerfile`, harness, `verification.json` |
| `fuzzing/afl-native/<format>/<ecosystem>/<slug>/` | AFL++ overlay and feedback receipt for the matching project |
| `fuzzing/fandango/` | Pinned Fandango environment, local `.fan` specs, and route decisions |
| `adapters/` | Catalog verification adapters and source locks |
| `lead-probes/` | Probes kept as evidence for leads that were checked and not counted |
| `scripts/` | Verification, capture, build, audit, and generation tools |
| `tests/` | Unit tests (`python3 -m unittest discover -s tests -q`) |
| `website/` | Static site generator for parsarium.com; built from the data on every push to `main` |

## Rules that do not bend

- **Only qualified paths count.** A path needs a pinned release, a documented local input API, both valid controls matching an independent oracle, a Docker harness, parser-source line coverage, stable input-dependent AFL++ feedback, and a numeric adoption signal from the cell's allowed metric (PROTOCOL.md). Candidates that miss any check go to `leads.json` with the reason.
- **Never pad a cell or invent a metric.** A cell below ten records its search routes, limits, and blockers instead. Ten is a ceiling, not a target to reach at any cost.
- **State shared parser families.** Wrappers, forks, and bindings are recorded with the engine they share; byte-identical forks and predecessor copies are excluded.
- **Valid inputs only when building the catalog.** Do not run malformed-input, vulnerability, or resource-exhaustion experiments as part of curation, and never commit crashing inputs.
- **Keep standard/runtime APIs separate** from third-party paths in every count.
- **Generated files are outputs.** Change their sources, then regenerate (below). `scripts/build_readmes.py` overwrites catalog and project READMEs.

## Adding or changing a path

1. Record the evidence in the cell (`parsers.json`, `ranking.md`, `cell.json`, `registry-snapshot.json`; rejected candidates in `leads.json`).
2. Add the project under `projects/` and its overlay under `fuzzing/afl-native/`; follow an existing path in the same ecosystem and format.
3. Regenerate aggregates, in this order. Pass each project as a separate argument (zsh does not split a quoted variable):

   ```sh
   python3 scripts/refresh_smoke_batch.py FORMAT/ECOSYSTEM/SLUG [...]
   python3 scripts/build_matrix.py
   python3 scripts/audit_projects.py --write
   python3 scripts/build_readmes.py
   ```

   For the ten active formats, also run `python3 scripts/plan_curated_catalog.py --write`, `python3 scripts/audit_curated_metrics.py`, `python3 scripts/audit_popularity_coverage.py` and `python3 scripts/build_rankings.py`.

4. Run the gates below.

## Gates

CI (`.github/workflows/verify.yml`) runs these on Python 3.11 and 3.13; run them before every push:

```sh
python3 scripts/validate_catalog.py
python3 scripts/audit_projects.py
python3 scripts/audit_fuzzing.py
python3 -m unittest discover -s tests -q
python3 website/build.py
python3 scripts/build_readmes.py --check
git diff --check
```

Code must run on Python 3.11: no backslashes inside f-string expressions.

## Practical notes

- Docker builds target Linux amd64 and arm64. A project's `verification.json` records the image ID and toolchain it was verified with.
- Adoption metrics are captured with timestamps and response hashes; recapture rather than editing numbers.
- Recorded commands in receipts write the repository root as `$PARSARIUM_HOME`; never commit absolute paths from your machine.
- Some managed-language overlays fix hash seeds or random sources so AFL++ feedback is repeatable. Each one is disclosed in its receipt; keep that disclosure when you touch the overlay.
- The website reads everything from the repository. To preview: `python3 website/build.py` and serve `website/dist`.
