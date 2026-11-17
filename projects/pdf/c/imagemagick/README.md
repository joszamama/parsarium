# imagemagick — PDF / C

Pinned release: `7.1.2-35`. [Manifest](manifest.json) · [Docker receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/pdf/c/imagemagick/verification.json)

[API, control result, and parser family](../../../../catalog/pdf/c/imagemagick/README.md)

The C harness calls `MagickReadImage` on a private local PDF. ImageMagick's PDF coder reads the media box and hands the file to Ghostscript `10.08.0`. The image links `libgs` in process and has no `gs` executable. The valid one-page control returns 612 × 792; coverage reaches 337 ImageMagick PDF coder lines and 5,685 Ghostscript PDF interpreter lines. PNG readback is reported separately. This path shares ImageMagick's PDF coder with its C++ entry point and Ghostscript's PDF interpreter with the direct Ghostscript paths.

## Run from the repository root

```sh
python3 parsarium.py build pdf c imagemagick
python3 parsarium.py run pdf c imagemagick controls/pdf/one-page.pdf
python3 parsarium.py replay pdf c imagemagick CORPUS_DIR runs/pdf-imagemagick-replay
python3 parsarium.py afl build pdf c imagemagick
python3 fuzzing/afl-native/pdf/c/imagemagick/source_feedback.py
python3 parsarium.py afl prepare pdf c imagemagick runs/pdf-imagemagick-afl
python3 parsarium.py afl run runs/pdf-imagemagick-afl --check
```

The [valid two-page comparison](../../../../fuzzing/afl-native/pdf/c/imagemagick/source-feedback.json) changed hit counts on 78 PDF coder lines and 2,918 Ghostscript PDF interpreter lines, adding 47 AFL++ edges. `source_feedback.py` reproduces the comparison using only these two valid controls.
