# resvg — SVG / C

Pinned release: `0.50.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/c/resvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg c resvg
python3 parsarium.py run svg c resvg controls/svg/red-green.svg
python3 parsarium.py replay svg c resvg CORPUS_DIR runs/svg-resvg-replay
python3 parsarium.py afl build svg c resvg
python3 parsarium.py afl prepare svg c resvg runs/svg-resvg-afl
```

Replace `CORPUS_DIR` with a directory of SVG files. The AFL++ command prepares a seeded run; it does not start a campaign.

The harness passes each input to `resvg_parse_tree_from_file` and reports image dimensions and the first two rendered RGB pixels. A valid one-pixel SVG reports `second: null`. The tagged C API shares the `resvg`/`usvg` Rust parser family with the C++ path.

**Coverage limit:** The base libFuzzer target instruments the C harness. The AFL++ `/work/replay @@` target has guards only in the Rust `usvg` parser crate. Replay is one process per file because the selected C API reads a local path.
