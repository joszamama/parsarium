# ImageMagick — PDF / C++

Pinned release: ImageMagick `7.1.2-35` with Ghostscript `10.08.0` as the PDF interpreter. The C++ harness writes bytes to a private local PDF and calls `Magick::readImages`; the valid one-page control reports one 612 × 792 page. See the [manifest](manifest.json), [Docker receipt](verification.json), and [AFL++ receipt](../../../../fuzzing/afl-native/pdf/cpp/imagemagick/verification.json).

The control reaches 337 ImageMagick PDF coder source lines and 5,685 Ghostscript PDF interpreter lines. Both libraries are built from pinned source with LLVM coverage, and Ghostscript is linked in process without a `gs` executable. Magick++ wrapper and PNG readback coverage are reported separately. The C and C++ ImageMagick entry points share their PDF coder and Ghostscript parser family.

```sh
python3 parsarium.py build pdf cpp imagemagick
python3 parsarium.py run pdf cpp imagemagick controls/pdf/one-page.pdf
python3 parsarium.py replay pdf cpp imagemagick CORPUS_DIR runs/imagemagick-cpp-pdf-replay
python3 parsarium.py afl build pdf cpp imagemagick
python3 fuzzing/afl-native/pdf/cpp/imagemagick/source_feedback.py
python3 parsarium.py afl prepare pdf cpp imagemagick runs/imagemagick-cpp-pdf-afl
python3 parsarium.py afl run runs/imagemagick-cpp-pdf-afl --check
```

The AFL++ control produced 15,094 edges. A [second valid two-page PDF](../../../../fuzzing/afl-native/pdf/cpp/imagemagick/source-feedback.json) added 59 stable edges across two fixed-input probes. `source_feedback.py` reproduces the comparison.
