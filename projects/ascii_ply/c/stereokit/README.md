# stereokit — ASCII PLY / C

Pinned release: `v0.3.11`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/c/stereokit/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply c stereokit
python3 parsarium.py run ascii_ply c stereokit controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply c stereokit CORPUS_DIR runs/ascii_ply-stereokit-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build ascii_ply c stereokit
python3 parsarium.py afl prepare ascii_ply c stereokit runs/ascii_ply-stereokit-afl --fandango 100
python3 parsarium.py afl run runs/ascii_ply-stereokit-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** The C header needs one generated compatibility fix for an unguarded C++ default argument; tagged library source is unchanged. Full graphics initialization retains allocations after shutdown, so fixed-input /work/fuzzer replay disables leak checking while /work/fuzzer-bin exposes the original sanitizer behavior. AFL++ uses /work/replay @@ because StereoKit initializes offscreen Mesa per process.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
