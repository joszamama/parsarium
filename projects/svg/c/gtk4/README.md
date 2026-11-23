# gtk4 — SVG / C

Pinned release: `4.24.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/c/gtk4/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg c gtk4
python3 parsarium.py run svg c gtk4 controls/svg/red-green.svg
python3 parsarium.py replay svg c gtk4 CORPUS_DIR runs/svg-gtk4-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build svg c gtk4
python3 parsarium.py afl prepare svg c gtk4 runs/svg-gtk4-afl --fandango 100
python3 parsarium.py afl run runs/svg-gtk4-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Sanitizer exception:** GTK/X11/Mesa retain process-global initialization allocations after fixed-input parsing. The container disables only LeakSanitizer's exit-time leak check; the fuzzer executable retains AddressSanitizer and UBSan while source-built GTK is separately instrumented for LLVM line coverage and AFL++.
