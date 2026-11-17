# qtbase — ASCII PNM / C++

Pinned release: `6.12.0`. [Manifest](manifest.json) · [Docker receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/ascii_pnm/cpp/qtbase/verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/cpp/qtbase/README.md)

The Docker build compiles QtBase from the pinned source archive with LLVM source coverage, so coverage reaches the PNM decoder in `src/gui/image/qppmhandler.cpp`. The harness writes the input to a local file and reads it with `QImageReader(path, "ppm")` with format auto-detection turned off, so only the built-in PNM handler can decode it. Inputs over 1 MiB are rejected. QtBase is licensed under LGPL-3.0-only.

The valid 2×1 P3 control passed Docker replay and one-case fuzzer smoke, covering 737 QtBase source lines, including 113 in `qppmhandler.cpp`. A separate valid 1×1 P3 file also parses. The source-built AFL++ overlay reported 2,210 feedback edges on the control; repeat maps matched, and the valid 1×1 image changed six edge IDs. The base libFuzzer binary has harness feedback only; use the AFL++ overlay for QtBase parser steering.

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm cpp qtbase
python3 parsarium.py run ascii_pnm cpp qtbase controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm cpp qtbase CORPUS_DIR runs/ascii_pnm-qtbase-replay
python3 parsarium.py afl build ascii_pnm cpp qtbase
python3 parsarium.py afl prepare ascii_pnm cpp qtbase runs/ascii_pnm-qtbase-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
