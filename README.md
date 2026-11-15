# Parsarium

The [website](website/README.md) helps users choose a format, find a documented parser, and open a runnable target. It is built from the committed catalog and deploys as a static GitHub Pages site.

Parsarium is a format-first catalog and target set for parser experiments. It verifies open-source libraries and standard APIs that parse local inputs in ten formats across C, C++, Go, Java, JavaScript, Python, Rust, and PHP. Selected paths have containerized, instrumented harnesses that accept local inputs and generated corpora. Each verified catalog entry has a pinned release, parser API, valid control, observed result, and evidence. Popularity ranks verified third-party packages **within a format and ecosystem**; the rankings do not compare ecosystems or imply independent parser engines.

The catalog currently contains **1,636 verified third-party package paths** in **80 format × ecosystem cells**. Seventy-nine cells meet the working goal of 20; PHP × ASCII PLY has five. **83 project harnesses** are runnable in containers: 82 third-party paths and one Python standard-library API. A catalog entry without a project harness remains documented but is not runnable through the commands below.

## Start here

Requirements: Python 3.11+ and Docker with Linux amd64 and arm64 support for container runs. Catalog browsing requires only Python. Commands run from the repository root.

```sh
python3 parsarium.py list --format png
python3 parsarium.py catalog png python
python3 parsarium.py projects --format png
python3 parsarium.py show png python pypng
python3 parsarium.py run png python pypng controls/png/red-green.png
```

`list` shows verified and runnable counts per cell. `catalog` shows the ranking, metric, search limits, and unresolved leads. `projects` lists container harnesses. `show` displays a harness's pinned release, parser API, control, and fuzz engine. `run` returns a JSON receipt for one supplied file; `status: ok` means the harness completed, not necessarily that the parser accepted the input. `--json` is available for `list`, `catalog`, `projects`, and `show`.

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
| `controls/<format>/` | Small valid inputs used for parser verification |
| `projects/<format>/<ecosystem>/<slug>/` | Dockerfile, byte-input harness, manifest, and coverage receipt |
| `fuzzing/afl-native/<format>/<ecosystem>/<slug>/` | AFL++ overlay and feedback receipt |
| `adapters/` | Catalog verification adapters and source locks |
| `scripts/` | Rebuild, audit, and discovery utilities |

The [selection protocol](PROTOCOL.md) defines parser eligibility, ranking, stopping rules, and uncertainty. The [project guide](projects/README.md) describes the harness contract. `python3 scripts/validate_catalog.py` checks catalog data; `python3 scripts/audit_fuzzing.py` checks the committed harness and AFL++ receipts.

The valid controls cover specific format subsets. A successful control does not establish support for every variant, security, or resource limits. Package paths that share an underlying parser are identified in the catalog. AFL++ feedback counts from different instrumentation methods are not comparable.
