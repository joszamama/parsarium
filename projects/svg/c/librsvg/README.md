# librsvg — SVG / C

Pinned release: `2.63.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/c/librsvg/README.md)

The exact 2 × 1 control passes with 2,949 covered librsvg Rust engine lines, including 177 SVG XML loader lines and 112 XML tree builder lines. The valid 1 × 1 control also passes. AFL++ recorded 5,214 control edges; 5,211 appeared in all three fixed control probes, and a second valid SVG had 302 stable edge IDs absent from every control probe.

The harness writes up to 1 MiB of bytes to `input.svg` in a fresh private directory under `/tmp` and passes that filename to `rsvg_handle_new_from_file`. It reads the size with `rsvg_handle_get_intrinsic_size_in_pixels`, renders with `rsvg_handle_render_document` into a Cairo ARGB32 surface, and reports width, height, and the first two pixels as straight RGB. A 1 × 1 document is accepted with `second: null`. Sizes are rounded up to whole pixels, and canvases larger than 4096 × 4096 pixels are rejected before rendering. librsvg resolves relative references only below the input's own directory, so the private directory keeps them inside the harness's own files.

The image builds librsvg from the pinned GNOME source archive with Meson. Its Rust dependencies come from the archive's own `Cargo.lock` (`cargo fetch --locked`), built with Rust 1.92.0 (LLVM 21, matching Ubuntu's clang and llvm-cov 21) and cargo-c 0.10.21. GdkPixbuf support, the pixbuf loader, and `rsvg-convert` are disabled; this path is the C API only. XML tokenization is Ubuntu's libxml2, which is not instrumented.

- Replay coverage: LLVM source coverage in librsvg's Rust engine (`/work/librsvg/rsvg/src/`). The control check fails unless lines are covered in the engine, in the SAX loader `xml/xml2_load.rs`, in the element-tree builder `xml/mod.rs`, and in the C API crate (`/work/librsvg/librsvg-c/src/`). The parser count in the receipt is the engine alone; the C API lines are reported separately.
- AFL++ overlay ([`fuzzing/afl-native/svg/c/librsvg`](../../../../fuzzing/afl-native/svg/c/librsvg/)): librsvg's Rust crates are built with SanitizerCoverage pcguard edges. `librsvg-2.so` is a direct dependency of the harness, so its edges register before the fork server starts. The harness is not instrumented, so every AFL++ edge comes from `librsvg-2.so`. The overlay check also runs a second valid SVG that draws with a path instead of rects and requires its tuple set to differ from the control's, showing that the feedback follows the parsed SVG content in the Rust engine.
- libFuzzer `fuzzer`: gets feedback only from the harness. librsvg is not built with libFuzzer instrumentation.

## Run from the repository root

```sh
python3 parsarium.py build svg c librsvg
python3 parsarium.py run svg c librsvg controls/svg/red-green.svg
python3 parsarium.py replay svg c librsvg CORPUS_DIR runs/svg-librsvg-replay
python3 parsarium.py afl build svg c librsvg
python3 parsarium.py afl prepare svg c librsvg runs/svg-librsvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
