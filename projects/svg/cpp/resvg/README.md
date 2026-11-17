# resvg — SVG / C++

Pinned release: `0.50.0`. The C++17 harness writes input bytes to a private local file, parses it with `resvg_parse_tree_from_file`, reads the size with `resvg_get_image_size`, and renders it with `resvg_render`. The valid control is 2 × 1 with a red first pixel and a green second pixel; [`one-pixel.svg`](one-pixel.svg) is 1 × 1 red.

The [Docker receipt](verification.json) records 1,133 executed lines in usvg's Rust SVG parser, including 234 in `svgtree/parse.rs`. This C++ call site shares the source archive, Cargo.lock, Rust 1.92.0 toolchain and parser family with [C resvg](../../c/resvg/). See the [manifest](manifest.json) and [AFL++ receipt](../../../../fuzzing/afl-native/svg/cpp/resvg/verification.json).

```sh
python3 parsarium.py build svg cpp resvg
python3 parsarium.py run svg cpp resvg controls/svg/red-green.svg
python3 parsarium.py replay svg cpp resvg CORPUS_DIR runs/svg-resvg-cpp-replay
python3 parsarium.py afl build svg cpp resvg
python3 parsarium.py afl prepare svg cpp resvg runs/svg-resvg-cpp-afl
python3 parsarium.py afl run runs/svg-resvg-cpp-afl --check
```

The AFL++ overlay instruments only the usvg crate; the C++ harness and renderer crates carry no guards. The control produced 1,238 edges, identical across three probes. A [second valid SVG](../../../../fuzzing/afl-native/svg/cpp/resvg/feedback-validation.json) added 30 stable edges.

**Coverage limit:** The AFL++ target uses one-shot `/work/replay @@` because the selected C API parses a local file; parser-source feedback comes from usvg Rust code.
