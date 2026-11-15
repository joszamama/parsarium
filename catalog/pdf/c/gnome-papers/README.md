# gnome-papers — PDF / C

- **Pinned release:** `51.1`
- **License:** GPL-2.0-or-later
- **Parsed scope:** PDF document page count
- **Underlying family:** GNOME Papers PDF backend over Poppler GLib
- **Local input API:** `pps_init(); g_filename_to_uri(local path); pps_document_factory_get_document(uri, error); pps_document_load(document, uri, error); pps_document_get_n_pages(document)`
- **Documentation:** [API reference](<https://gnome.pages.gitlab.gnome.org/papers/document/class.Document.html>)
- **Catalog evidence:** [parser record](../../../../data/c/pdf/parsers.json) · [control verification](../../../../data/c/pdf/verification.json) · [within-ecosystem ranking](../../../../data/c/pdf/ranking.md)
- **Valid control:** [`controls/pdf/two-page.pdf`](../../../../controls/pdf/two-page.pdf)

## Observed control result

```json
{
  "pages": 2
}
```

Distinct documented C document-library input API, sharing the Poppler GLib PDF engine with poppler-glib, Evince, and libvips. The public umbrella header requires a macro claiming author contact; the adapter mirrors signatures from hash-pinned headers rather than defining that macro. The API is explicitly unstable.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
