# gdk-pixbuf — SVG / C++

Pinned release: `2.44.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/cpp/gdk-pixbuf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg cpp gdk_pixbuf
python3 parsarium.py run svg cpp gdk_pixbuf controls/svg/red-green.svg
python3 parsarium.py replay svg cpp gdk_pixbuf CORPUS_DIR runs/svg-gdk_pixbuf-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build svg cpp gdk_pixbuf
python3 parsarium.py afl prepare svg cpp gdk_pixbuf runs/svg-gdk_pixbuf-afl --fandango 100
python3 parsarium.py afl run runs/svg-gdk_pixbuf-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** The C++17 harness calls the GDK-Pixbuf C file API. GDK-Pixbuf and its C++ wrapper share the same librsvg SVG syntax engine; the base libFuzzer target instruments the C++ harness, while AFL++ /work/replay provides librsvg parser feedback.
