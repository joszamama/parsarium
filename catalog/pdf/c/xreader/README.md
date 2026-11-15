# xreader — PDF / C

- **Pinned release:** `4.6.10`
- **License:** GPL-2.0
- **Parsed scope:** PDF page count through source-built Xreader libdocument C API
- **Underlying family:** Xreader PDF backend over Poppler GLib
- **Local input API:** `ev_init(); g_filename_to_uri(local path); ev_document_factory_get_document(uri, error); ev_document_get_n_pages(document)`
- **Documentation:** [API reference](<https://github.com/linuxmint/xreader/blob/master.mint27/libdocument/ev-document-factory.h>)
- **Catalog evidence:** [parser record](../../../../data/c/pdf/parsers.json) · [control verification](../../../../data/c/pdf/verification.json) · [within-ecosystem ranking](../../../../data/c/pdf/ranking.md)
- **Valid control:** [`controls/pdf/two-page.pdf`](../../../../controls/pdf/two-page.pdf)

## Observed control result

```json
{
  "pages": 2
}
```

Xreader is an Evince-derived package with its own source-built libdocument C API and PDF backend. Its tagged Meson build links poppler-glib for PDF; this is another package input path over the already counted Poppler syntax engine. No comparable Homebrew formula requested-install count exists for Xreader.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
