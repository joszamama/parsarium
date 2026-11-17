# gpac — MP4 / C++

Pinned release: `26.07.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/cpp/gpac/README.md)

`harness.cpp` compiles the selected call site, `adapters/cpp/mp4/gpac.cpp`, as C++17. That file includes the C call site, so C and C++ share one GPAC parser. `adapter/` holds exact copies of both files because Docker only sees this directory. The image build checks their SHA-256 values.

The harness renames the call site's `main` and `printf` so it can call it per input. It also deletes a `GF_ISOFile` the call site leaves open on an early return. The GPAC calls and their arguments are unchanged.

The exact control covers 2,421 GPAC ISO media parser lines and 22 selected call-site lines. AFL++ reports 2,383 edges. A second valid three-second MP4 also passes the one-case runner and changes 124 edge IDs.

## Run from the repository root

```sh
python3 parsarium.py build mp4 cpp gpac
python3 parsarium.py run mp4 cpp gpac controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 cpp gpac CORPUS_DIR runs/mp4-cpp-gpac-replay
python3 parsarium.py afl build mp4 cpp gpac
python3 parsarium.py afl prepare mp4 cpp gpac runs/mp4-cpp-gpac-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
