# atril — PDF / C

- **Pinned release:** `1.28.2`
- **License:** GPL-2.0-or-later
- **Parsed scope:** PDF page count through Atril libdocument C API
- **Underlying family:** Atril PDF backend over Poppler GLib
- **Local input API:** `ev_init(); g_filename_to_uri(local path); ev_document_factory_get_document(uri, error); ev_document_get_n_pages(document)`
- **Documentation:** [API reference](<https://github.com/mate-desktop/atril/blob/v1.28.2/libdocument/ev-document-factory.h>)
- **Catalog evidence:** [parser record](../../../../data/c/pdf/parsers.json) · [control verification](../../../../data/c/pdf/verification.json) · [within-ecosystem ranking](../../../../data/c/pdf/ranking.md)
- **Valid control:** [`controls/pdf/two-page.pdf`](../../../../controls/pdf/two-page.pdf)

## Observed control result

```json
{
  "pages": 2
}
```

Atril is an Evince-derived package with its own public libdocument C API and PDF backend. The pinned backend links Poppler GLib; it adds a package input path, not an independent PDF syntax engine. Ubuntu arm64 binaries and official tagged source are pinned; no comparable Homebrew formula requested-install count is available.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
