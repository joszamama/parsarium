# evince — PDF / C

- **Pinned release:** `48.4`
- **License:** GPL-2.0-or-later
- **Parsed scope:** PDF page count through Evince libdocument C API
- **Underlying family:** Evince PDF backend over Poppler GLib
- **Local input API:** `ev_init(); ev_document_factory_get_document_for_gfile(GFile from local path, ...); ev_document_get_n_pages()`
- **Documentation:** [API reference](<https://gnome.pages.gitlab.gnome.org/evince/document/class.Document.html>)
- **Catalog evidence:** [parser record](../../../../data/c/pdf/parsers.json) · [control verification](../../../../data/c/pdf/verification.json) · [within-ecosystem ranking](../../../../data/c/pdf/ranking.md)
- **Valid control:** [`controls/pdf/two-page.pdf`](../../../../controls/pdf/two-page.pdf)

## Observed control result

```json
{
  "pages": 2
}
```

Evince's public C libdocument factory loads the local PDF; the installed libpdfdocument backend directly links the Poppler GLib library already counted in this cell. This is a package path, not an independent PDF syntax engine.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
