# fltk — ASCII PNM / Rust

Pinned release: `fltk` and `fltk-sys` `1.5.23`, with vendored FLTK `1.4.5`. The adapter writes input bytes to a private `.ppm` file and calls `PnmImage::load(path)`, then reads dimensions and RGB data. The valid 2 × 1 control yields red and green pixels.

The Rust API reaches FLTK's C++ `Fl_PNM_Image` through the cfltk shim. The [Docker receipt](verification.json) records 32 executed Rust crate lines, 403 underlying native source lines, and 60 in the PNM loader. This is the FLTK parser family behind the Rust binding; see the [manifest](manifest.json) and [source lock](source-lock.json).

```sh
python3 parsarium.py build ascii_pnm rust fltk
python3 parsarium.py run ascii_pnm rust fltk controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm rust fltk CORPUS_DIR runs/fltk-pnm-replay
python3 parsarium.py afl build ascii_pnm rust fltk
python3 fuzzing/afl-native/ascii_pnm/rust/fltk/verify_valid_variant.py
python3 parsarium.py afl prepare ascii_pnm rust fltk runs/fltk-pnm-afl
python3 parsarium.py afl run runs/fltk-pnm-afl --check
```

The [AFL++ overlay](../../../../fuzzing/afl-native/ascii_pnm/rust/fltk) builds the Rust target both with and without native FLTK/cfltk instrumentation. The verified control produced 433 AFL++ tuples with native instrumentation and 208 with Rust instrumentation alone; the native build also has more guard slots. A [second valid PGM](../../../../fuzzing/afl-native/ascii_pnm/rust/fltk/valid-variant.json) reached 7 additional native PNM source regions and 7 stable new AFL++ edges. AFL++ consumes input through its shared memory or stdin channel. The overlay uses vendored source, while the catalog's earlier control run used an upstream prebuilt FLTK artifact; both return the same result.
