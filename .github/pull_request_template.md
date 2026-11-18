## What this changes

<!-- One target or one tool per pull request. Link the issue if there is one. -->

## Checklist

- [ ] New or changed parser paths meet every rule in [PROTOCOL.md](https://github.com/joszamama/parsarium/blob/main/PROTOCOL.md): pinned release, documented input API, both valid controls matching the oracle, Docker harness with parser-source coverage, stable AFL++ feedback, adoption metric with source and date, parser family stated.
- [ ] Derived files were regenerated with the scripts listed in [AGENTS.md](https://github.com/joszamama/parsarium/blob/main/AGENTS.md), not edited by hand.
- [ ] No malformed, crashing or resource-exhausting inputs, secrets, or absolute local paths are committed.
- [ ] The CI checks pass locally:
  `validate_catalog.py`, `audit_projects.py`, `audit_fuzzing.py`, `unittest discover -s tests`, `website/build.py`, `build_readmes.py --check`.
