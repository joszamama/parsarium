# bit7z — ZIP / C++

Pinned release: `4.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/cpp/bit7z/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip cpp bit7z
python3 parsarium.py run zip cpp bit7z controls/zip/hello.zip
python3 parsarium.py replay zip cpp bit7z CORPUS_DIR runs/zip-bit7z-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build zip cpp bit7z
python3 parsarium.py afl prepare zip cpp bit7z runs/zip-bit7z-afl --fandango 100
python3 parsarium.py afl run runs/zip-bit7z-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Sanitizer exception:** SevenZip performs unaligned integer loads on the valid ZIP control, so the fuzzer disables only UBSan's alignment check. The AFL++ overlay also disables UBSan's function-type check for AFL's compiler wrapper. bit7z and SevenZip both define COM GUID constants, so ASan's duplicate-global ODR check is disabled at load; ASan memory checks and other UBSan checks remain enabled.
