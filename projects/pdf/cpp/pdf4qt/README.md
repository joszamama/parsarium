# pdf4qt — PDF / C++

Pinned release: `1.6.0.0`. [Manifest](manifest.json) · [Docker receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/pdf/cpp/pdf4qt/verification.json)

[API and catalog evidence](../../../../catalog/pdf/cpp/pdf4qt/README.md)

Replay calls `pdf::PDFDocumentReader::readFromFile()` on a local PDF and reports `PDFDocument::getCatalog()->getPageCount()`. The byte-input fuzzer calls the same native PDF reader's documented `readFromBuffer()` API. The pinned Blend2D dependency is built without JIT; it is a renderer, not a PDF parser. Inputs are limited to 1 MiB.

The valid one-page control covers 1,551 PDF4QT library source lines, including 288 in `pdfdocumentreader.cpp` and 358 in `pdfparser.cpp`. The [AFL++ source allowlist](afl-allowlist.txt) limits feedback to those two files. A [fixed valid-variant check](../../../../fuzzing/afl-native/pdf/cpp/pdf4qt/source-feedback.json) records 394 parser edges for the one-page PDF and 395 for a two-page PDF. Each input produced identical edge IDs in three fresh-container runs.

## Run from the repository root

```sh
python3 parsarium.py build pdf cpp pdf4qt
python3 parsarium.py run pdf cpp pdf4qt controls/pdf/one-page.pdf
python3 parsarium.py replay pdf cpp pdf4qt CORPUS_DIR runs/pdf-pdf4qt-replay
python3 parsarium.py afl build pdf cpp pdf4qt
python3 parsarium.py afl prepare pdf cpp pdf4qt runs/pdf-pdf4qt-afl
```

The AFL++ command prepares a seeded run; it does not start a campaign. The target reads each file at `@@`.
