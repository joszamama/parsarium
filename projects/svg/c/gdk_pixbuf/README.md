# gdk-pixbuf — SVG / C

Pinned release: `2.44.8`, with the SVG loader plugin and parser from librsvg `2.63.4`. [Manifest](manifest.json)

[API, control result, and parser family](../../../../catalog/svg/c/gdk-pixbuf/README.md)

The [Docker control receipt](verification.json) records an exact 2×1 red/green SVG render, 840 covered GDK-Pixbuf source lines, 69 SVG loader plugin lines, and 3,020 librsvg Rust core lines, including 177 in `xml2_load.rs`. The [AFL++ receipt](../../../../fuzzing/afl-native/svg/c/gdk_pixbuf/verification.json) records source-built parser feedback on the same valid control.

The harness passes up to 1 MiB of bytes to `gdk_pixbuf_loader_new_with_type("svg")`, then `gdk_pixbuf_loader_write` and `gdk_pixbuf_loader_close`. It checks that the loader format is `svg` and reports width, height, and the first two RGBA pixels. For a one-pixel image, `second` is `null`. Canvases larger than 4096 × 4096 pixels are rejected before rendering.

GdkPixbuf does not parse SVG itself. Its SVG module, `libpixbufloader_svg.so`, comes from librsvg and passes the bytes to librsvg's Rust parser. The image builds both from pinned GNOME source archives. librsvg's Rust dependencies come from its own `Cargo.lock` (`cargo fetch --locked`), built with Rust 1.92.0 (LLVM 21) and cargo-c 0.10.21.

- Replay coverage: LLVM source coverage over GdkPixbuf (`/work/source/gdk-pixbuf/`) and librsvg (`/work/librsvg/rsvg/src/`, including `xml/xml2_load.rs` and the loader plugin). The run fails if either side has no covered lines.
- AFL++ overlay: librsvg's Rust crates and the loader plugin are built with SanitizerCoverage pcguard edges, and the plugin is preloaded so its edges register before the fork server starts. The one-shot target is `/work/replay @@`; the harness and GdkPixbuf are not instrumented in the overlay, so every AFL++ edge on the control comes from the librsvg stack. The [fixed-input feedback check](../../../../fuzzing/afl-native/svg/c/gdk_pixbuf/feedback-validation.json) records the small repeat variation and stable edges unique to a valid SVG `<path>` variant.
- libFuzzer `fuzzer`: gets feedback only from the harness. librsvg is not built with libFuzzer instrumentation.

## Run from the repository root

```sh
python3 parsarium.py build svg c gdk_pixbuf
python3 parsarium.py run svg c gdk_pixbuf controls/svg/red-green.svg
python3 parsarium.py replay svg c gdk_pixbuf CORPUS_DIR runs/svg-gdk_pixbuf-replay
python3 parsarium.py afl build svg c gdk_pixbuf
python3 parsarium.py afl prepare svg c gdk_pixbuf runs/svg-gdk_pixbuf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
