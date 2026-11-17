# gdk-pixbuf — SVG / C++

Pinned release: `2.44.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/cpp/gdk-pixbuf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg cpp gdk_pixbuf
python3 parsarium.py run svg cpp gdk_pixbuf controls/svg/red-green.svg
python3 parsarium.py replay svg cpp gdk_pixbuf CORPUS_DIR runs/svg-gdk_pixbuf-replay
python3 parsarium.py afl build svg cpp gdk_pixbuf
python3 parsarium.py afl prepare svg cpp gdk_pixbuf runs/svg-gdk_pixbuf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** The C++17 harness calls the GDK-Pixbuf C file API. GDK-Pixbuf and its C++ wrapper share the same librsvg SVG syntax engine; the base libFuzzer target instruments the C++ harness, while AFL++ /work/replay provides librsvg parser feedback.
