# External fuzzing workflow

Parsarium keeps parser packages and their pinned, covered harnesses in
`projects/`. The commands here prepare inputs, launchers, and results outside
those packages. Parser library source is not patched for Fandango or AFL++.

## One-input contract

`scripts/run_case.py FORMAT ECOSYSTEM PACKAGE_SLUG FILE` executes a supplied
file once through the project's existing fuzz entry point. It verifies the
project receipt, uses the image's declared platform, builds the image if
missing, runs without network access, and records a JSON result. All 83 current
project entries passed this route on their valid controls; see
`data/fuzz-case-smoke.json`. The 83 entries cover 80 third-party cells, two
additional third-party projects, and one standard API project.

The result status is `ok`, `target_nonzero`, `timeout`, `input_too_large`, or
`infrastructure_error`. `ok` means the fuzz target executed without an
uncaught failure; it **does not** prove that the parser accepted the input.
`target_nonzero` is a lead for replay and triage, not a vulnerability claim.
The JSON includes the input SHA-256, container image ID, elapsed time, exit
code, and bounded output tails. Inputs are limited to 1 MiB, matching the
current harnesses. A timed-out container is forcibly removed.

For a single input:

```sh
python3 scripts/run_case.py png c libpng controls/png/red-green.png
```

## Fandango as an input generator

Fandango 1.3+ can fetch a ready-made PNG specification with `-F png`. See the
[Fanbase guide](https://fandango-fuzzer.github.io/Fanbase.html). The
Fanbase registry can change, so preserve the generated corpus and record the
exact generator command. Check `fanbase list` before assuming a Fanbase spec
exists for another format; use `-f local-spec.fan` when it does not.

```sh
fandango fuzz -F png -n 1000 -d generated/png
python3 scripts/replay_corpus.py png c libpng generated/png runs/png-libpng-fandango \
  --generator Fandango --generator-version "$(fandango --version)" --spec png \
  --generator-command 'fandango fuzz -F png -n 1000 -d generated/png'
```

`replay_corpus.py` copies unique inputs to `runs/.../inputs/` under their
SHA-256 names, runs the chosen project on each, and writes per-input receipts
plus `summary.json`. It replays C, C++, Go, Java, JavaScript, Python, and Rust
corpora in one container with zero mutation iterations. PHP uses its
`run-single` entry for each input. If a batch fails, the runner isolates each
case and records the batch log. Use `--per-case` to request individual replay
from the start. The runner continues through target failures and timeouts. The
preserved inputs can be replayed even if the remote Fanbase spec later changes.
For bit-for-bit regeneration, pin and archive the Fandango version and the
complete local specification and its dependencies as well. A local spec's hash
can be recorded with `--spec-sha256`.

## AFL++ feedback for C and C++

`scripts/build_afl_native.py` derives an external AFL++ build from each
verified C or C++ project. It keeps the project's pinned parser source and
byte-input harness, recompiles them with Ubuntu's pinned AFL++ 4.33c package,
and requires `afl-showmap` to report nonzero feedback edges when replaying the
valid control. The overlay receipt records the image ID, package version,
control, required AFL++ map size, and number of feedback edges. The existing
project image and its LLVM
source-coverage receipt are left intact. Function-pointer type checking is
disabled in these overlays because PDFio's valid control trips that UBSan
check; AddressSanitizer and the other undefined-behavior checks remain enabled.

```sh
python3 scripts/build_afl_native.py --all
python3 scripts/prepare_afl_run.py pdf c pdfio runs/pdfio-afl
python3 scripts/prepare_afl_run.py png c libpng runs/png-afl --seed-dir generated/png
```

The second command copies the valid control into `runs/pdfio-afl/seeds/`,
writes `plan.json`, and prints an exact Docker command. It does **not** start
`afl-fuzz`. Add `--seed-dir generated/pdf` to include a generated corpus.
When a researcher runs the printed command, AFL++ reads the seeds from
`/seeds`, mutates in memory through its libFuzzer-compatible driver, and
writes to `runs/pdfio-afl/afl-out/`. Its live edge map steers mutation; the
`afl-showmap` count is only a preflight check. AFL++ saves interesting inputs
in `queue/`, potential crashes in `crashes/`, potential timeouts in `hangs/`,
and progress fields in `fuzzer_stats`. These are findings to reproduce and
triage, not confirmed defects. See the [AFL++ workflow](https://aflplus.plus/docs/fuzzing_in_depth/)
for its seed, queue, and feedback model.

After a researcher stops a campaign:

```sh
python3 scripts/summarize_afl_run.py runs/pdfio-afl
```

This writes `runs/pdfio-afl/afl-summary.json` with the AFL++ statistics and
hashes of every saved queue, crash, and hang file. `plan.json` contains a
resume command using `-i -`. Generated inputs can be used as AFL++ seeds, but
the black-box and grey-box results stay in separate run directories.

## Native coverage-guided campaigns in all eight ecosystems

Every project also has a plan for its existing fuzz engine: libFuzzer in C,
C++, and Rust; Go native fuzzing; Jazzer in Java; Jazzer.js in JavaScript;
Atheris in Python; and PHP-Fuzzer in PHP. Their feedback counts are not
comparable across ecosystems.

```sh
python3 scripts/prepare_native_run.py png javascript pngjs runs/pngjs-native \
  --seed-dir generated/png --duration-seconds 3600
python3 scripts/run_prepared_native.py runs/pngjs-native --check
python3 scripts/run_prepared_native.py runs/pngjs-native
```

Preparation copies and hashes the valid control plus optional supplied seeds,
pins the verified image ID, and writes `plan.json` with an exact Docker
command. `--check` validates the plan and seeds without starting a campaign.
The final command starts mutation and records `campaign.log` and
`campaign.json`. The engine receives writable corpus and artifact directories.
Go seeds are encoded as Go fuzz corpus files; its generated coverage corpus is
stored separately in `go-cache/`. PHP-Fuzzer updates its corpus in place. It
has no engine duration flag, so the runner stops its container at the
requested duration. Other engines receive their own duration flag, with a
short shutdown allowance in the runner.

The plan preflight passed for all 83 current projects; see
`data/native-plan-smoke.json`. It verifies plan construction, pinned images,
seeds, and command structure. It does not prove that a full campaign will run
to completion. The one-input and batch replays above verify valid controls
through the same fuzz targets. Engine details: [Go](https://go.dev/doc/security/fuzz/),
[Jazzer](https://github.com/CodeIntelligenceTesting/jazzer),
[Jazzer.js](https://github.com/CodeIntelligenceTesting/jazzer.js/blob/main/docs/fuzz-settings.md),
[Atheris](https://github.com/google/atheris), and
[PHP-Fuzzer](https://github.com/nikic/PHP-Fuzzer).

The run layouts are:

```text
runs/<fandango-run>/inputs/       preserved generated bytes, named by SHA-256
runs/<fandango-run>/executions/   per-input JSON results
runs/<fandango-run>/summary.json  generation and replay metadata
runs/<afl-run>/seeds/            immutable seed copies
runs/<afl-run>/plan.json         exact image, map size, command, and resume command
runs/<afl-run>/afl-out/          AFL++ queue, crashes, hangs, and fuzzer_stats
runs/<afl-run>/afl-summary.json  post-run inventory and hashes
runs/<native-run>/corpus/       writable seed and interesting-input corpus
runs/<native-run>/artifacts/    engine-saved findings and reproducers
runs/<native-run>/go-cache/     Go generated coverage corpus, when applicable
runs/<native-run>/plan.json     pinned image, seeds, duration, and Docker command
runs/<native-run>/campaign.log  engine progress and feedback reports
runs/<native-run>/campaign.json execution status, timing, image, and log hash
```

## Scope and comparison

The one-input bridge and native engine plans work across all eight ecosystems.
The source-level AFL++ overlay is verified for all 21 current C and C++ paths.
Keep the parser project, seed set, time budget,
platform, and input limit in each run plan. Do not compare AFL++ edge counts
with LLVM line coverage or with edge counts from a different parser build.

The preparation and smoke commands execute valid controls only. They do not
start a fuzz campaign or perform malformed-input experiments.

Run `python3 scripts/smoke_case_bridge.py` to repeat all one-input control
checks, `python3 scripts/smoke_corpus_batch.py` to repeat the no-mutation
batch checks, `python3 scripts/smoke_native_plans.py` to repeat native plan
preflights, and `python3 scripts/audit_fuzzing.py` to check the committed
receipts.
