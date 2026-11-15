# zathura-pdf-poppler — PDF / C

- **Pinned release:** `2026.07.18`
- **License:** Zlib
- **Parsed scope:** Two-page PDF page count through released C plugin document-open callback
- **Underlying family:** Zathura PDF Poppler plugin over Poppler GLib
- **Local input API:** `pdf_document_open(zathura_document_t*) callback, called with a host document whose path resolves to the supplied local PDF; zathura_document_get_number_of_pages(document)`
- **Documentation:** [API reference](<https://pwmt.org/projects/zathura/plugins/development/>)
- **Catalog evidence:** [parser record](../../../../data/c/pdf/parsers.json) · [control verification](../../../../data/c/pdf/verification.json) · [within-ecosystem ranking](../../../../data/c/pdf/ranking.md)
- **Valid control:** [`controls/pdf/two-page.pdf`](../../../../controls/pdf/two-page.pdf)

## Observed control result

```json
{
  "pages": 2,
  "has_parser_data": true
}
```

The published plugin is a distinct Zlib-licensed C package path, but its PDF syntax engine is Poppler GLib, already represented separately. The adapter compiles the unmodified released document.c with matching pinned Zathura host headers and a minimal shim for the documented host accessors. It checks callback page count and parser data; full viewer registration and rendering are outside the verified scope.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
