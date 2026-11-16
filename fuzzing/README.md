# Running parser harnesses

Every project accepts a local byte input. The [main CLI](../README.md) lists runnable projects and routes inputs to their pinned container images. Fuzzing runs write under `runs/`, which is ignored by Git. Commands below run from a clone; with the [package](https://pypi.org/project/parsarium/), use `parsarium` in place of `python3 parsarium.py`.

## One input or an external corpus

```sh
python3 parsarium.py run png c stb controls/png/red-green.png
python3 parsarium.py replay png c stb generated/png runs/stb-replay \
  --generator Fandango --spec png
```

`run` writes a JSON result with the input hash, image ID, exit status, and elapsed time. `ok` means the harness completed; parser acceptance is not inferred from that status. `target_nonzero` and `timeout` are observations requiring replay and triage. Inputs are limited to 1 MiB.

`replay` preserves unique inputs by SHA-256, runs the selected harness, and writes per-input receipts and `summary.json`. Most ecosystems use one-container batch replay when possible; PHP uses individual runs. `--per-case` forces individual replay. Generator metadata can include `--generator-version`, `--spec`, and `--generator-command`.

[Fandango and Fanbase](https://fandango-fuzzer.github.io/Fanbase.html) provide an external generation route. The available specs are listed by `fanbase list`; `-F png` downloads the default PNG spec. A local `.fan` specification can be used with Fandango's `-f` option. Generated files are ordinary corpus inputs for `replay` or `afl prepare --seed-dir`.

## AFL++

Every runnable project has a verified AFL++ overlay. The feedback source depends on the ecosystem:

| Ecosystem | AFL++ feedback |
| --- | --- |
| C, C++ | Compiled parser edges |
| Rust | Compiled parser edges through afl.rs |
| Go | Covered parser-package statement blocks |
| Java | JaCoCo-covered parser source lines |
| JavaScript | Executed V8 parser source ranges |
| Python | Executed parser source lines |
| PHP | Xdebug-covered parser source lines |

A few targets wrap a native library from a managed language; their overlays take edges from the pinned shared library instead, and their receipts say so.

For Go, Java, JavaScript, Python, and PHP, a small instrumented proxy maps parser features into AFL++'s shared feedback map. The parser packages remain unchanged. These bridges are slower than native instrumentation, and their feature and tuple counts are not comparable across ecosystems. Hash collisions in the 64 KiB map are possible. The PHP bridge treats ordinary `Exception` values as parser rejections; PHP `Error` values and process failures remain fatal.

```sh
python3 parsarium.py afl build ascii_ply python plyfile
python3 parsarium.py afl prepare ascii_ply python plyfile runs/plyfile-afl
python3 parsarium.py afl run runs/plyfile-afl --check
python3 parsarium.py afl run runs/plyfile-afl --seconds 3600
python3 parsarium.py afl summary runs/plyfile-afl
```

`afl build` creates the selected local image and verifies its parser coverage. A fresh checkout needs this step before preparation. `afl prepare` copies the project's valid control into `seeds/`, checks the overlay receipt and local image, and writes `plan.json`. Additional inputs enter with repeated `--seed FILE` or `--seed-dir DIRECTORY`. `afl run` checks the plan, image, and seed hashes before starting a time-bounded campaign. `--resume` continues the same `afl-out/` directory. `afl summary` inventories queue, crash, and hang files with hashes and reads AFL++'s `fuzzer_stats`.

Five short campaigns exercised the Go, Java, JavaScript, Python, and PHP bridges; [campaign receipts](../data/afl-campaign-smoke.json) record actual executions and statistics. [Differential checks](../data/afl-feedback-differential.json) show that input-dependent parser features change AFL++ feedback in each of those ecosystems. [Plan preflights](../data/afl-plan-smoke.json) prepare a run for every overlay. These checks establish runnable launchers and feedback, not parser safety.

## Ecosystem fuzz engines

Each project also includes its native fuzz entry point: libFuzzer for C, C++, and Rust; Go native fuzzing; Jazzer for Java; Jazzer.js for JavaScript; Atheris for Python; and PHP-Fuzzer for PHP.

```sh
python3 parsarium.py build png javascript pngjs
python3 parsarium.py native prepare png javascript pngjs runs/pngjs-native \
  --duration-seconds 3600
python3 parsarium.py native run runs/pngjs-native --check
python3 parsarium.py native run runs/pngjs-native
```

`native prepare` records the seed hashes, pinned image, engine, duration, and command. `native run` writes `campaign.log` and `campaign.json`. Engine feedback counters differ in meaning and should not be compared between ecosystems.

## Run files

| Path | Contents |
| --- | --- |
| `runs/<replay>/inputs/` | Preserved external inputs named by SHA-256 |
| `runs/<replay>/executions/` | Per-input results |
| `runs/<replay>/summary.json` | Corpus and generator metadata |
| `runs/<afl>/plan.json` | Pinned image, seeds, feedback kind, and AFL++ command |
| `runs/<afl>/afl-out/` | AFL++ queue, potential crashes, hangs, and statistics |
| `runs/<afl>/campaign.json` | Execution time, status, and log hash |
| `runs/<afl>/afl-summary.json` | Saved-file inventory and `fuzzer_stats` |
| `runs/<native>/campaign.json` | Native engine execution receipt |

Potential crashes and hangs are leads. A saved case requires reproduction and parser-specific triage before any defect claim.
