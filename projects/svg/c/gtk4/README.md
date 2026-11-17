# gtk4 — SVG / C

Pinned release: `4.24.1`. [Manifest](manifest.json) · [Docker receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/svg/c/gtk4/verification.json)

[API, catalog evidence, and parser family](../../../../catalog/svg/c/gtk4/README.md)

The harness passes input bytes in `GBytes` to `gtk_svg_new_from_bytes()` and reports the paintable's intrinsic width and height. The source-built native GTK 4 parser under `gtk/svg/` is instrumented. Xvfb supplies the display needed by `gtk_init()`; no pixel rendering is requested. Inputs are limited to 1 MiB. The alternate valid SVG uses a path element and has intrinsic size `4×2`.

The `2×1` control covered 1,673 GTK `gtk/svg/` source lines, including 509 in `gtksvgparser.c`. AFL++ feedback is scoped to GTK's SVG parser translation unit with the [source allowlist](afl-allowlist.txt), excluding display initialization. A [fixed valid-variant check](../../../../fuzzing/afl-native/svg/c/gtk4/source-feedback.json) records 187 control edges and 196 edges on the `4×2` SVG. The valid variant adds 9 parser edge IDs. Each input produced the same edge IDs in nine repeated one-input runs.

GTK/X11/Mesa retain process-global initialization allocations after a one-input run. The container disables only LeakSanitizer's exit-time leak check. The fuzzer executable retains ASan and UBSan; GTK itself has LLVM line coverage and AFL++ instrumentation.

## Run from the repository root

```sh
python3 parsarium.py build svg c gtk4
python3 parsarium.py run svg c gtk4 controls/svg/red-green.svg
python3 parsarium.py replay svg c gtk4 CORPUS_DIR runs/svg-gtk4-replay
python3 parsarium.py afl build svg c gtk4
python3 parsarium.py afl prepare svg c gtk4 runs/svg-gtk4-afl
```

Replace `CORPUS_DIR` with a directory of valid SVG files. The AFL++ command prepares a seeded run; it does not start a campaign. The prepared target reads a file at `@@`.
