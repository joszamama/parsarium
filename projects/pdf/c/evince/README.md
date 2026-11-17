# evince — PDF / C

Pinned release: `48.4`. [Manifest](manifest.json) · [Docker receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/pdf/c/evince/verification.json)

[API and catalog evidence](../../../../catalog/pdf/c/evince/README.md)

Replay calls Evince's public `ev_document_factory_get_document_for_gfile()` on a local PDF and reports `ev_document_get_n_pages()`. The byte-input fuzzer writes a temporary file and uses Evince's public `ev_document_factory_get_document_for_fd()` with the PDF MIME type. Both routes invoke the pinned Evince PDF backend, source-built Poppler GLib, and its PDF core. This is a separate package entry with a shared Poppler parser family; it is not an independent PDF syntax engine. Inputs are limited to 1 MiB.

The valid two-page control covers 262 Evince PDF backend lines, 73 document-factory lines, 357 Poppler GLib lines, and 1,679 Poppler core lines through the GFile route. The FD fuzzer route separately covers 258 backend lines, including `load_fd`, 300 Poppler GLib document lines, and 1,677 Poppler core lines. The [AFL++ source allowlist](afl-allowlist.txt) limits feedback to the Evince PDF backend and Poppler parser files. Three fresh-container runs of each valid control produced identical edge IDs: 577 for the two-page PDF and 572 for the one-page PDF.

## Run from the repository root

```sh
python3 parsarium.py build pdf c evince
python3 parsarium.py run pdf c evince controls/pdf/two-page.pdf
python3 parsarium.py replay pdf c evince CORPUS_DIR runs/pdf-evince-replay
python3 parsarium.py afl build pdf c evince
python3 parsarium.py afl prepare pdf c evince runs/pdf-evince-afl
```

The AFL++ command prepares a seeded run; it does not start a campaign. The target reads each file at `@@`. See the [fixed valid-control feedback check](../../../../fuzzing/afl-native/pdf/c/evince/source-feedback.json) for observed parser edges.
