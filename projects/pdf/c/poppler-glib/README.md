# poppler-glib — PDF / C

Pinned release: `26.11.0`. [Manifest](manifest.json) · [source lock](source-lock.json)

[API, control result, and parser family](../../../../catalog/pdf/c/poppler-glib/README.md)

The harness copies the input into a `GBytes`, calls `poppler_document_new_from_bytes`, and reports `poppler_document_get_n_pages`. Inputs over 8 MiB, documents that fail to load (including locked ones), and page counts outside 1–100000 are rejected.

The build compiles only Poppler core and the GLib frontend. The GLib frontend requires Cairo, so Poppler's Cairo output device is built into `libpoppler-glib`. The C++ and Qt frontends, GObject introspection, GTK demos and tests, utilities, Boost, PNG, image codecs, color management, network, signature backends, HarfBuzz, and font discovery are off. Coverage is gated on the GLib frontend (`glib/`, including `poppler-document.cc`) and on Poppler core (`poppler/`, including `Parser.cc`, `Lexer.cc`, `XRef.cc`, and `PDFDoc.cc`).

Poppler's GLib C and C++ frontends wrap the same core parser. They count as one Poppler parser family; the [C++ project](../../cpp/poppler/README.md) covers the other frontend.

The pinned one-page control passed the Docker replay and one-case fuzzer smoke. It covered 84 Poppler GLib frontend lines and 1,243 underlying Poppler core lines, including `Parser.cc`, `Lexer.cc`, `XRef.cc`, and `PDFDoc.cc`. The AFL++ overlay rebuilt the parser with AFL++ instrumentation and observed 1,067 feedback edges on the same control. See the [Docker receipt](verification.json) and [AFL++ receipt](../../../../fuzzing/afl-native/pdf/c/poppler-glib/verification.json).

## Run from the repository root

```sh
python3 parsarium.py build pdf c poppler-glib
python3 parsarium.py run pdf c poppler-glib controls/pdf/one-page.pdf
python3 parsarium.py replay pdf c poppler-glib CORPUS_DIR runs/pdf-poppler-glib-replay
python3 parsarium.py afl build pdf c poppler-glib
python3 parsarium.py afl prepare pdf c poppler-glib runs/pdf-poppler-glib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
