# wxwidgets — ASCII PNM / C++

Pinned release: `3.3.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, catalog evidence, and parser family](../../../../catalog/ascii_pnm/cpp/wxwidgets/README.md)

The harness registers `wxPNMHandler`, passes each local file to `wxImage::LoadFile`, and reports the decoded dimensions and first two RGBA pixels. A one-pixel image reports `second: null`. The Docker build links the pinned native wxWidgets PNM handler into the target and records covered lines in `src/common/imagpnm.cpp`. Xvfb supplies wxGTK's display while the target runs.

The control decodes to `2×1` with a red pixel followed by a green pixel. A second valid P2 control (`black-white.pgm`) decodes to black and white. The P3 control also passes twice in one fuzzer process; this checks persistent wxWidgets initialization without generating inputs. The AFL++ overlay uses a source allowlist for `imagpnm.cpp`. Its [feedback check](../../../../fuzzing/afl-native/ascii_pnm/cpp/wxwidgets/source-feedback.json) records distinct edge maps for the two valid PNM variants.

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm cpp wxwidgets
python3 parsarium.py run ascii_pnm cpp wxwidgets controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm cpp wxwidgets CORPUS_DIR runs/ascii_pnm-wxwidgets-replay
python3 parsarium.py afl build ascii_pnm cpp wxwidgets
python3 parsarium.py afl prepare ascii_pnm cpp wxwidgets runs/ascii_pnm-wxwidgets-afl
```

Replace `CORPUS_DIR` with a directory of PNM files. The AFL++ command prepares a seeded run; it does not start a campaign. AFL++ instrumentation is limited to wxWidgets' PNM source file.
