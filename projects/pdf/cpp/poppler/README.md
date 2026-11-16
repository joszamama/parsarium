# poppler — PDF / C++

Pinned release: `26.11.0`. [Manifest](manifest.json) · [source lock](source-lock.json)

[API, control result, and parser family](../../../../catalog/pdf/cpp/poppler/README.md)

The harness calls `poppler::document::load_from_file` on a temporary `.pdf` copy of the input and reports `pages()`. Inputs over 8 MiB, locked documents, and page counts outside 1–100000 are rejected.

The build compiles only Poppler core and the C++ frontend. GLib, Qt, utilities, Cairo, Boost, image codecs, color management, network, signature backends, and font discovery are off. Coverage is gated on the C++ frontend (`cpp/`, including `poppler-document.cpp`) and on Poppler core (`poppler/`, including `Parser.cc`, `Lexer.cc`, `XRef.cc`, and `PDFDoc.cc`).

Poppler's C++ and GLib C frontends wrap the same core parser. They count as one Poppler parser family.

The pinned one-page control passed the Docker replay and one-case fuzzer smoke. It covered 39 Poppler C++ frontend lines and 1,196 underlying Poppler core lines, including `Parser.cc`, `Lexer.cc`, `XRef.cc`, and `PDFDoc.cc`. The AFL++ overlay rebuilt the parser with AFL++ instrumentation and observed 953 feedback edges on the same control. See the [Docker receipt](verification.json) and [AFL++ receipt](../../../../fuzzing/afl-native/pdf/cpp/poppler/verification.json).

## Run from the repository root

```sh
python3 parsarium.py build pdf cpp poppler
python3 parsarium.py run pdf cpp poppler controls/pdf/one-page.pdf
python3 parsarium.py replay pdf cpp poppler CORPUS_DIR runs/pdf-poppler-replay
python3 parsarium.py afl build pdf cpp poppler
python3 parsarium.py afl prepare pdf cpp poppler runs/pdf-poppler-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
