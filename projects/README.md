# Parser harnesses

`projects/<format>/<ecosystem>/<slug>/` contains one runnable parser path. The collection has 83 projects across all 80 cells: 82 third-party package paths and CPython's `wave` API. Other verified catalog packages remain in `data/` until a harness and container are verified.

Each project includes:

| File | Purpose |
| --- | --- |
| `manifest.json` | Pinned package or runtime, source hash, control, expected output, fuzz engine, and coverage subject |
| `Dockerfile` | Parser and harness build for the declared Linux platform |
| `harness.*` | Local byte-input parser call and observable format-specific result |
| `fuzz.*` or equivalent | Entry point for the ecosystem fuzz engine |
| `run-control.*` | Valid-control replay with parser-source coverage |
| `verification.json` | Observed output, covered parser source, toolchain, and image ID |

The harness reads supplied bytes or a temporary local file and calls the parser's documented API. Generic file I/O and a hard-coded expected result do not qualify. Verification requires a passing valid control and coverage in parser source, separate from coverage in the harness. Shared underlying parser families are recorded in the catalog.

```sh
python3 parsarium.py projects --format pdf
python3 parsarium.py show pdf java pdfbox
python3 parsarium.py build pdf java pdfbox
python3 parsarium.py run pdf java pdfbox controls/pdf/one-page.pdf
```

A project can be rebuilt and its control rechecked with `python3 scripts/run_project.py FORMAT ECOSYSTEM SLUG`. `python3 scripts/audit_projects.py --check` compares manifests and receipts with the catalog. Builds can depend on package repositories or system packages beyond the pinned parser source; `verification.json` records the observed image and toolchain. Image IDs are checked before prepared fuzz runs.

The [fuzzing guide](../fuzzing/README.md) covers AFL++, native engines, external corpora, and run artifacts. A project receipt proves its stated control and coverage conditions; it does not establish behavior on other inputs.
