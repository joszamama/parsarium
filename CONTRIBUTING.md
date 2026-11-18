# Contributing

Thank you for helping. Parsarium is useful only if every number in it can be checked, so contributions follow the same rules as the existing catalog.

## Ways to help

- **Suggest a parser.** Open an issue with the package, the format, the language, a link to its documented API for reading local bytes or files, and its adoption metric for that language ([PROTOCOL.md](PROTOCOL.md) lists the metric per ecosystem). Packages that miss a rule are still worth reporting; they are recorded as leads with the reason.
- **Report a wrong record.** If a release, license, family, adoption number, or link is wrong, open an issue with the evidence. Maintainers of a listed package can also ask for a different description or for removal ([ETHICS.md](ETHICS.md)).
- **Fix a harness or script.** Pull requests are welcome; keep each one to a single target or tool.
- **Security problems in Parsarium itself** go through [SECURITY.md](SECURITY.md), not public issues.

## What a new parser path needs

A path counts only when it has all of these (details in [PROTOCOL.md](PROTOCOL.md)):

1. a pinned release and its license;
2. a documented API that reads local bytes or a local file;
3. both valid controls for the format, with output that matches the independent oracle;
4. a Docker harness under `projects/<format>/<ecosystem>/<slug>/` with coverage in the parser's own source;
5. an AFL++ overlay under `fuzzing/afl-native/<format>/<ecosystem>/<slug>/` with stable feedback that differs between the controls;
6. the cell's adoption metric, captured with its source and date;
7. the parser family it shares with other paths, if any.

Do not add malformed, crashing, or resource-exhausting inputs to the repository. Every committed input must be a valid file of its format.

## Workflow

[AGENTS.md](AGENTS.md) maps the repository and lists the order for regenerating derived files. Before opening a pull request, run the checks that CI runs:

```sh
python3 scripts/validate_catalog.py
python3 scripts/audit_projects.py
python3 scripts/audit_fuzzing.py
python3 -m unittest discover -s tests -q
python3 website/build.py
python3 scripts/build_readmes.py --check
```

Code must run on Python 3.11. Generated files (`data/cells.json`, `data/pilot-cells.json`, `data/projects-coverage.json`, smoke reports, and the catalog and project READMEs) are rebuilt by scripts; change their sources instead of editing them.

By contributing you agree that your contribution is licensed under the [Apache License 2.0](LICENSE).
