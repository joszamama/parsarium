# StereoKit — ASCII PLY / C

Pinned release: `v0.3.11`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/c/stereokit/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply c stereokit
python3 parsarium.py run ascii_ply c stereokit controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply c stereokit CORPUS_DIR runs/ply-stereokit-replay
python3 parsarium.py afl build ascii_ply c stereokit
python3 parsarium.py afl prepare ascii_ply c stereokit runs/ply-stereokit-afl
```

Replace `CORPUS_DIR` with a directory of ASCII PLY files. The AFL++ command prepares a seeded run; it does not start a campaign.

The harness calls the public `model_create_file` C API with a local `.ply` file, then reads mesh vertices and indices. StereoKit's tagged `model_ply.cpp` includes the bundled `micro_ply` syntax parser, which is also used by `sk_renderer`; the two packages have a shared parser family.

**Coverage limit:** The pinned public C header has one unguarded C++ default argument. The Docker build makes a generated C-compatible header copy without changing the tagged library source. The full graphics runtime retains allocations after shutdown, so fixed-input `/work/fuzzer` replay disables leak checking; `/work/fuzzer-bin` keeps the upstream lifecycle visible for separate investigation. AFL++ runs `/work/replay @@` as one process per file because StereoKit initializes offscreen Mesa. Native in-process campaigns are unsupported for this harness.
