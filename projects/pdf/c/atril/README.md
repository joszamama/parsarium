# atril — PDF / C

Pinned release: `1.28.2`. [Manifest](manifest.json) · [source lock](source-lock.json) · [control receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/pdf/c/atril/verification.json)

[API and catalog evidence](../../../../catalog/pdf/c/atril/README.md)

The harness calls Atril's public libdocument factory on a local PDF and reports `ev_document_get_n_pages()`. Atril 1.28.2 has no GFile factory, so the harness builds a `GFile` from the local path and passes its `file://` URI to `ev_document_factory_get_document()`. The fuzzer accepts up to 1 MiB and writes each input to a temporary `.pdf` file first.

Atril's URI factory retains a 16-byte GLib MIME string on the valid control. The target disables LeakSanitizer for this known process-lifetime allocation; AddressSanitizer and UndefinedBehaviorSanitizer remain enabled.

Atril is an Evince fork. Its PDF backend (`backend/pdf/ev-poppler.cc`) calls Poppler GLib, and Poppler's core makes every PDF syntax decision. This build uses the same Poppler 26.11.0 archive as the Poppler GLib, Evince and GNOME Papers projects. Treat it as a separate package path over one shared parser family, not as an independent PDF parser.

Both sources are pinned by SHA-256: the official Atril release tarball and the Poppler archive. Key source members are checked again after extraction. Only `libdocument` and the PDF backend are compiled. Both carry LLVM source coverage, as do Poppler GLib and the Poppler core. AFL++ instruments the backend and the Poppler parser files listed in [afl-allowlist.txt](afl-allowlist.txt).

The control check replays [`two-page.pdf`](../../../../controls/pdf/two-page.pdf) (expects `{"pages":2}`) and a second valid file, [`valid-one-page.pdf`](valid-one-page.pdf) (a copy of `controls/pdf/one-page.pdf`, expects `{"pages":1}`). It then compares which backend and Poppler regions each file executes, and how often.

The control covers 240 Atril backend lines and 1,557 Poppler core lines. AFL++ feedback is limited to the PDF backend, Poppler GLib, and Poppler core libraries: 550 stable control edges across three fresh runs. The valid one-page PDF has five fewer edge IDs and changes 99 stable hit-count buckets. [Valid-variant receipt](../../../../fuzzing/afl-native/pdf/c/atril/valid-variant.json).

## Run from the repository root

```sh
python3 parsarium.py build pdf c atril
python3 parsarium.py run pdf c atril controls/pdf/two-page.pdf
python3 parsarium.py replay pdf c atril CORPUS_DIR runs/pdf-atril-replay
python3 parsarium.py afl build pdf c atril
python3 parsarium.py afl prepare pdf c atril runs/pdf-atril-afl
python3 parsarium.py afl run runs/pdf-atril-afl --check
python3 fuzzing/afl-native/pdf/c/atril/verify_valid_variant.py
```

Replace `CORPUS_DIR` with a directory of PDF files. The AFL++ prepare command seeds a run but does not start a campaign. The target reads each file at `@@`. The last command needs the AFL++ image built first. It compares AFL++ edges for the two valid PDFs and writes `valid-variant.json`.
