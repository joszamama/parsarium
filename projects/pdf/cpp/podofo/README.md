# podofo — PDF / C++

Pinned release: `1.1.2`. [Manifest](manifest.json) · [source lock](source-lock.json)

[API, control result, and parser family](../../../../catalog/pdf/cpp/podofo/README.md)

The harness writes each input to a temporary local PDF, then calls `PoDoFo::PdfMemDocument::Load(path)` and `GetPages().GetCount()`. Inputs are capped at 8 MiB, PoDoFo's object count is capped at 1,048,575, and PoDoFo logging is off. The Docker build checks the source archive SHA-256 and the PdfMemDocument, tokenizer, and parser source files against the [source lock](source-lock.json). The control gate requires LLVM source coverage in `PdfParser.cpp`, `PdfParserObject.cpp`, `PdfTokenizer.cpp`, `PdfMemDocument.cpp`, and `PdfPageCollection.cpp`.

PoDoFo is its own parser family. It does not share parser code with Poppler.

The valid one-page PDF control passed Docker replay and one-case fuzzer smoke. A separate valid zero-page PDF reports `pages: 0`. The replay covered 2,378 pinned PoDoFo source lines, including the parser and tokenizer. The AFL++ overlay builds the PoDoFo library with AFL instrumentation and reported 1,263 feedback edges on the control. The base image's libFuzzer binary has harness feedback only; use the AFL++ overlay for parser steering. [Docker receipt](verification.json) and [AFL++ receipt](../../../../fuzzing/afl-native/pdf/cpp/podofo/verification.json) bind the source, image, and control.

## Run from the repository root

```sh
python3 parsarium.py build pdf cpp podofo
python3 parsarium.py run pdf cpp podofo controls/pdf/one-page.pdf
python3 parsarium.py replay pdf cpp podofo CORPUS_DIR runs/pdf-podofo-replay
python3 parsarium.py afl build pdf cpp podofo
python3 parsarium.py afl prepare pdf cpp podofo runs/pdf-podofo-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
