# graphicsmagick — PDF / C

Pinned release: `1.3.49`, with Ghostscript `10.08.0` as the PDF interpreter. [Manifest](manifest.json) · [Docker receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/pdf/c/graphicsmagick/verification.json)

[API, control result, and parser family](../../../../catalog/pdf/c/graphicsmagick/README.md)

The harness calls `MagickReadImage()` on a local temporary file and reports the page count plus the first page's width and height. GraphicsMagick's PDF coder hands the file to Ghostscript, which interprets it with its pdfi PDF interpreter. Both libraries are built from pinned source with LLVM coverage. GraphicsMagick is compiled with `HasGSLIB` and linked to `libgs`, so Ghostscript runs in the same process instead of as a spawned `gs` program. The image contains no `gs` executable. Inputs are limited to 8 MiB.

The one-page control reports `612×792`; a separate valid two-page PDF reports two pages at the same first-page size. The control covers 200 GraphicsMagick PDF coder lines, 229 delegate lines, and 5,685 Ghostscript `pdf/` lines, including 128 in `pdf_xref.c`. The AFL++ overlay records 13,536 edges on the control. A [fixed valid-variant check](../../../../fuzzing/afl-native/pdf/c/graphicsmagick/source-feedback.json) finds 49 different edge IDs for the two-page PDF. The prepared AFL command uses `@@` file input.

## Run from the repository root

```sh
python3 parsarium.py build pdf c graphicsmagick
python3 parsarium.py run pdf c graphicsmagick controls/pdf/one-page.pdf
python3 parsarium.py replay pdf c graphicsmagick CORPUS_DIR runs/pdf-graphicsmagick-replay
python3 parsarium.py afl build pdf c graphicsmagick
python3 parsarium.py afl prepare pdf c graphicsmagick runs/pdf-graphicsmagick-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
