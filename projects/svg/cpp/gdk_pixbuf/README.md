# gdk-pixbuf — SVG / C++

This C++17 harness calls GDK-Pixbuf `2.44.8` through its documented [`gdk_pixbuf_new_from_file(local SVG path)`](https://docs.gtk.org/gdk-pixbuf/ctor.Pixbuf.new_from_file.html) API. It first calls [`gdk_pixbuf_get_file_info`](https://docs.gtk.org/gdk-pixbuf/type_func.Pixbuf.get_file_info.html) to confirm the SVG loader and cap the decoded canvas at 4096 × 4096 pixels. Bytes supplied by an external tool are written to a temporary local `.svg` file, parsed, rendered, and reported as dimensions and RGBA pixel samples. For a one-pixel image, `second` is `null`.

GDK-Pixbuf delegates SVG syntax and rendering to the librsvg `2.63.4` loader plugin. This is a separate C++ package input path over the same underlying parser family as GDK-Pixbuf's C API and librsvg itself. The Docker build pins the GDK-Pixbuf and librsvg source archives, librsvg's `Cargo.lock`, Rust 1.92.0, and the Ubuntu base image. The valid control covers 992 GDK-Pixbuf lines, 70 SVG loader plugin lines, and 3,020 librsvg Rust core lines, including 177 in `xml2_load.rs`. The AFL++ file target uses `/work/replay @@` with guard feedback only from librsvg core and plugin; its [fixed-input feedback check](../../../../fuzzing/afl-native/svg/cpp/gdk_pixbuf/feedback-validation.json) records 99.801% stable control edge IDs and 302 stable edges unique to a valid SVG path variant.

## Run from the repository root

```sh
python3 parsarium.py build svg cpp gdk_pixbuf
python3 parsarium.py run svg cpp gdk_pixbuf controls/svg/red-green.svg
python3 parsarium.py replay svg cpp gdk_pixbuf CORPUS_DIR runs/svg-gdk-pixbuf-cpp-replay
python3 parsarium.py afl build svg cpp gdk_pixbuf
python3 parsarium.py afl prepare svg cpp gdk_pixbuf runs/svg-gdk-pixbuf-cpp-afl
```

Replace `CORPUS_DIR` with a directory of SVG files. AFL++ preparation creates a seeded run without starting a campaign. See the [manifest](manifest.json), [control receipt](verification.json), [AFL++ receipt](../../../../fuzzing/afl-native/svg/cpp/gdk_pixbuf/verification.json), and [catalog record](../../../../catalog/svg/cpp/gdk-pixbuf/README.md).
