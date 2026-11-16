# @firecrawl/pdf-inspector-wasm — PDF / JavaScript

Pinned release: `1.25.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/javascript/firecrawl-pdf-inspector-wasm/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf javascript firecrawl_pdf_inspector_wasm
python3 parsarium.py run pdf javascript firecrawl_pdf_inspector_wasm controls/pdf/one-page.pdf
python3 parsarium.py replay pdf javascript firecrawl_pdf_inspector_wasm CORPUS_DIR runs/pdf-firecrawl_pdf_inspector_wasm-replay
python3 parsarium.py afl build pdf javascript firecrawl_pdf_inspector_wasm
python3 parsarium.py afl prepare pdf javascript firecrawl_pdf_inspector_wasm runs/pdf-firecrawl_pdf_inspector_wasm-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
