# Parsarium

The [website](https://parsarium.com/) helps users choose a format, find a documented parser, and open a runnable target. It is built from the committed catalog and hosted on GitHub Pages.

Parsarium is a format-first catalog and target set for parser experiments. It verifies open-source libraries and standard APIs that parse local inputs in ten formats across C, C++, Go, Java, JavaScript, Python, Rust, and PHP. Selected paths have containerized, instrumented harnesses that accept local inputs and generated corpora. Each verified catalog entry has a pinned release, parser API, valid control, observed result, and evidence. Popularity ranks verified third-party packages **within a format and ecosystem**; the rankings do not compare ecosystems or imply independent parser engines.

The catalog selects **775 control-verified third-party package paths** across ten formats and eight ecosystems. Each cell has at most ten; 74 of 80 reach ten, and the other six report the smaller supported count. Every selected path has a positive numeric adoption signal, though 48 use a separately labeled secondary source. The [curation record](data/curation/README.md) explains metrics, exclusions, and remaining uncertainty. The [current coverage report](data/projects-coverage.json) distinguishes fully verified harnesses from staged and pending paths; a catalog entry is runnable only when that report marks it verified.

## Start here

Requirements: Python 3.11+ and Docker with Linux amd64 and arm64 support for container runs. Catalog browsing requires only Python. Commands run from the repository root.

```sh
python3 parsarium.py list --format png
python3 parsarium.py catalog png python
python3 parsarium.py projects --format png
python3 parsarium.py show png python pypng
python3 parsarium.py run png python pypng controls/png/red-green.png
```

`list` shows verified and runnable counts for each format and ecosystem. `catalog` shows the ranking, metric, search limits, and unresolved leads. `projects` lists container harnesses. `show` displays a harness's pinned release, parser API, control, and fuzz engine. `run` returns a JSON receipt for one supplied file; `status: ok` means the harness completed, not necessarily that the parser accepted the input. `--json` is available for `list`, `catalog`, `projects`, and `show`.

Run every fully verified Docker target for one format with its own pinned control, or send the same file to each target. Results are saved under one directory, with a receipt per target and a `summary.json`:

```sh
python3 parsarium.py run-format png --list
python3 parsarium.py run-format png --results runs/png-controls
python3 parsarium.py run-format png --file my.png --results runs/png-my-file
```

Use `--ecosystem python` to narrow the batch. A shared file may be accepted by some parsers and rejected by others; the receipts record each outcome.

Formats: `png`, `zip`, `mp4`, `wav`, `pdf`, `svg`, `http11`, `ascii_ply`, `ascii_pnm`, `mp3_id3v2`. Ecosystems: `c`, `cpp`, `go`, `java`, `javascript`, `python`, `rust`, `php`.

## Fuzzing

Every runnable project has an AFL++ overlay with parser-dependent feedback. AFL++ instruments compiled C, C++, and Rust targets directly. Go, Java, JavaScript, Python, and PHP harnesses use parser coverage bridges. A prepared run includes a valid seed, pinned image ID, exact command, and output directory.

```sh
python3 parsarium.py afl build png python pypng
python3 parsarium.py afl prepare png python pypng runs/pypng-afl
python3 parsarium.py afl run runs/pypng-afl --check
python3 parsarium.py afl run runs/pypng-afl --seconds 60
python3 parsarium.py afl summary runs/pypng-afl
```

Additional seeds enter with `--seed FILE` or `--seed-dir DIRECTORY` on `afl prepare`. `afl run --resume` continues an existing output directory. AFL++ saves interesting inputs in `queue/`, potential crashes in `crashes/`, potential timeouts in `hangs/`, and progress in `fuzzer_stats`.

Each project also has a plan for its ecosystem fuzz engine:

```sh
python3 parsarium.py build png python pypng
python3 parsarium.py native prepare png python pypng runs/pypng-native --duration-seconds 60
python3 parsarium.py native run runs/pypng-native --check
python3 parsarium.py native run runs/pypng-native
```

[Fandango 1.3+ and Fanbase](https://fandango-fuzzer.github.io/Fanbase.html) can generate inputs externally. A generated corpus can be replayed through any matching project or added as AFL++ seeds:

```sh
fandango fuzz -F png -n 100 -d generated/png
python3 parsarium.py replay png python pypng generated/png runs/pypng-fandango \
  --generator Fandango --spec png
python3 parsarium.py afl prepare png python pypng runs/pypng-generated-afl \
  --seed-dir generated/png
```

The [fuzzing guide](fuzzing/README.md) describes feedback, run artifacts, and result interpretation.

## Evidence and layout

| Path | Contents |
| --- | --- |
| `data/<ecosystem>/<format>/` | Verified parsers, ranking, search leads, standard APIs, control results, and release evidence |
| `data/curation/` | Ten-path selection, pinned adoption sources, metric exceptions, and original verification evidence |
| `controls/<format>/` | Small valid inputs used for parser verification |
| `projects/<format>/<ecosystem>/<slug>/` | Dockerfile, byte-input harness, manifest, and coverage receipt |
| `fuzzing/afl-native/<format>/<ecosystem>/<slug>/` | AFL++ overlay and feedback receipt |
| `adapters/` | Catalog verification adapters and source locks |
| `scripts/` | Rebuild, audit, and discovery utilities |

The [selection protocol](PROTOCOL.md) defines parser eligibility, ranking, stopping rules, and uncertainty. The [project guide](projects/README.md) describes the harness contract. `python3 scripts/validate_catalog.py` checks catalog data; `python3 scripts/audit_fuzzing.py` checks the committed harness and AFL++ receipts.

The valid controls cover specific format subsets. A successful control does not establish support for every variant, security, or resource limits. Package paths that share an underlying parser are identified in the catalog. AFL++ feedback counts from different instrumentation methods are not comparable.
