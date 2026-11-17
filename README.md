# Parsarium

The [website](https://parsarium.com/) helps users choose a format, find a documented parser, and open a runnable target. It is built from the committed catalog and hosted on GitHub Pages.

Parsarium is a format-first catalog and target set for parser experiments. Its active collection covers ten formats across C, C++, Go, Java, JavaScript, Python, Rust, and PHP; JSON and XML are separate incomplete pilots. Selected third-party paths have containerized, instrumented harnesses that accept local inputs and generated corpora. Each verified catalog entry has a pinned release, parser API, valid control, observed result, and evidence. Popularity ranks verified third-party packages **within a format and ecosystem**; the rankings do not compare ecosystems or imply independent parser engines.

The active catalog selects **770 fully runnable third-party package paths** across ten formats and eight ecosystems. Each cell has at most ten; 71 of 80 reach ten, and the other nine report the smaller supported count. Every selected path has a positive numeric adoption signal, though 48 use a separately labeled secondary source. Five adopted, control-verified candidates lack verified parser feedback and are [excluded with their blockers recorded](data/curation/feedback-exclusions.json), without filling their slots with lower-ranked leads. The [curation record](data/curation/README.md) explains metrics and remaining uncertainty. Standard/runtime APIs and the incomplete pilot formats have [separate coverage counts](data/projects-coverage.json).

## Install

```sh
python3 -m pip install parsarium
parsarium list --format png
```

The package provides the `parsarium` command and a small Python API
(`from parsarium import catalog`). Each wheel bundles a versioned snapshot of
harnesses, controls, and catalog data. On first use it checks the snapshot's
SHA-256 and extracts it to your cache directory without a network request, so
each package version pins one snapshot. `parsarium run-selection MANIFEST` runs
a selection saved from the [bench](https://parsarium.com/bench/).

To work from a clone instead, install it in editable mode and point
`PARSARIUM_HOME` at it:

```sh
git clone https://github.com/joszamama/parsarium.git
cd parsarium
python3 -m pip install -e .
export PARSARIUM_HOME="$PWD"
```

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

Formats: `png`, `zip`, `mp4`, `wav`, `pdf`, `svg`, `http11`, `ascii_ply`, `ascii_pnm`, `mp3`, plus the `json` and `xml` pilots. Ecosystems: `c`, `cpp`, `go`, `java`, `javascript`, `python`, `rust`, `php`.

### MP3 targets

MP3 is one format. Each ecosystem keeps the ten most-adopted paths from the former MP3-with-ID3v2 and plain-MP3 cells ([merge record](data/curation/mp3-merge.json)). A path is verified either on the ID3v2-tagged control (`controls/mp3/id3v2-tagged-tone.mp3`) or on the untagged MPEG frame controls; its parser record says which (`control_kind`). Every MP3 target lives under `projects/mp3/` and uses the format name `mp3`, for example `python3 parsarium.py run mp3 java jaudiotagger controls/mp3/id3v2-tagged-tone.mp3`; `parsarium.py projects --format mp3` lists all of them.

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

After a run has saved queue files, `report --replay-queue` measures parser source lines reached by a bounded sample. It replays each selected input once in the project's verified coverage image; it does not start AFL++. LLVM-covered C, C++ and Rust merge profiles from `/work/replay`; Go replays one fuzz test corpus seed per input; Java replays literal verified harness commands and unions JaCoCo source lines, including pinned JDK module-patch paths. Python, PHP and JavaScript package paths use Python `trace`, PHP Xdebug or Node V8 coverage. The report records input hashes, both image IDs, and hashes of profiles or trace exports. The LWJGL/Assimp Java/native hybrid and the standard Node `JSON.parse` path are labeled unsupported for queue line replay; each has separate valid-control coverage and AFL feedback.

```sh
python3 parsarium.py report http11 cpp boost_beast runs/beast-afl \
  --output reports/beast-afl --replay-queue --max-queue-inputs 32
```

Each project also has a plan for its ecosystem fuzz engine:

```sh
python3 parsarium.py build png python pypng
python3 parsarium.py native prepare png python pypng runs/pypng-native --duration-seconds 60
python3 parsarium.py native run runs/pypng-native --check
python3 parsarium.py native run runs/pypng-native
```

[Fandango and Fanbase](https://fandango-fuzzer.github.io/Fanbase.html) generate inputs from format specifications. `fandango setup` installs Fandango 1.3.1 and its dependencies from a [hash-locked requirements file](fuzzing/fandango/requirements.lock) in the ignored local `.venv/`. `fandango generate` runs it for one verified project, writes a receipt, and can replay the corpus or prepare (not start) an AFL++ run:

On Linux arm64, install a C compiler before setup: the locked `accumulation-tree` release builds from source there.

```sh
python3 parsarium.py afl build png c lodepng
python3 parsarium.py fandango setup
python3 parsarium.py fandango generate png c lodepng runs/lodepng-fandango \
  --count 100 --seed 42 --replay --prepare-afl
python3 parsarium.py afl run runs/lodepng-fandango/afl --check
```

Fanbase supplies the default specs for `png`, `zip`, `wav`, `svg`, `json`, `xml`, and MP3 targets verified on the ID3v2-tagged control (`mp3` in Fanbase, including an ID3v2.3 tag). Parsarium supplies local specs for MP4, PDF, HTTP/1.1 requests, ASCII PLY, ASCII PNM P3, and MP3 targets verified on untagged Layer III frames. `--fanbase` selects a Fanbase variant such as `png-boundary`; `--spec` selects another local spec. All ten active formats and the JSON and XML pilots have a default generation route. The MP4 grammar includes one decodable 2×2 H.264 video frame and no audio track. Parsers may differ in which valid grammar variations they accept; replay records each outcome.

MP3 targets verified on untagged frames use a [local Layer III seed grammar](fuzzing/fandango/plain-mp3-decision.md). Fanbase's `-F mp3` grammar emits tags and Layer I/II frames, so it cannot be converted to those targets by stripping tags.

```sh
python3 parsarium.py fandango generate mp4 cpp exiv2 runs/exiv2-fandango \
  --count 100 --seed 42 --replay
```

The run directory must be new or empty, and inside this repository it must be under `runs/` or `generated/`, which Git ignores. It contains `generated/`, a copy or snapshot of the spec, and `fandango.json`. The receipt records the Fandango executable path, SHA-256, version, requirements-lock hash, and installed dependencies; the exact command and environment; the seed (`--random-seed`, also used as `PYTHONHASHSEED`); the spec hash; and each output's SHA-256 and size. `--fanbase-registry DIR` pins a local Fanbase checkout and checks the installed spec against its `index.yml`. Without it, the registry revision is not recorded; only the installed spec snapshot is. If Fandango fails, writes no files, or writes empty, oversized, or linked files, the command stops before replay or AFL++ preparation.

The [fuzzing guide](fuzzing/README.md) describes feedback, run artifacts, and result interpretation. Corpus replay reports show per-input outcomes. The optional AFL++ queue replay above measures aggregate source lines from saved queue inputs; without it, line views come from the pinned valid-control build.

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

## License

Parsarium is licensed under the [Apache License 2.0](LICENSE). Each parser keeps its own license, recorded in the catalog.

## Releasing the package

`.github/workflows/release.yml` publishes on a version tag. It builds the snapshot from the tagged commit with `scripts/build_snapshot.py` (byte-reproducible), embeds the snapshot and its SHA-256 in the wheel, smoke-tests the installed wheel outside the checkout, and uploads it to PyPI with trusted publishing.

1. Once: on PyPI, add a trusted publisher for project `parsarium`, owner `joszamama`, repository `parsarium`, workflow `release.yml`, environment `pypi`. On GitHub, create the `pypi` environment under Settings → Environments.
2. Set `__version__` in `src/parsarium/__init__.py` (calendar versions, such as `2026.11.16`), commit, and push.
3. Tag and push: `git tag v2026.11.16 && git push origin v2026.11.16`.
