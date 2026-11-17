# librsvg — SVG / C++

Pinned release: `2.63.4`. The C++17 adapter writes input bytes to a private local file, calls `rsvg_handle_new_from_file`, reads dimensions, and renders with `rsvg_handle_render_document`. The valid 2 × 1 control produces red and green pixels; a second valid 1 × 1 SVG is checked too.

This path uses the same pinned Rust SVG engine as [C librsvg](../../c/librsvg/). The C and C++ bindings are separate ecosystem entry points, but one underlying parser family. See the [manifest](manifest.json), [Docker receipt](verification.json), and [AFL++ receipt](../../../../fuzzing/afl-native/svg/cpp/librsvg/verification.json).

```sh
python3 parsarium.py build svg cpp librsvg
python3 parsarium.py run svg cpp librsvg controls/svg/red-green.svg
python3 parsarium.py replay svg cpp librsvg CORPUS_DIR runs/librsvg-cpp-replay
python3 parsarium.py afl build svg cpp librsvg
python3 parsarium.py afl prepare svg cpp librsvg runs/librsvg-cpp-afl
python3 parsarium.py afl run runs/librsvg-cpp-afl --check
```

The replay receipt records 2,949 executed Rust engine source lines, including 177 in the SVG XML loader. The AFL++ overlay instruments librsvg's Rust crates while leaving the C++ harness uninstrumented. It observed 5,204 control edges, 99.8% stable across three probes; a second valid SVG using a path added 302 stable edges. Ubuntu libxml2 performs XML tokenization without source instrumentation in this image.
