# poppler-glib — PDF / C

- **Pinned release:** `26.11.0`
- **Upstream:** [source repository](<https://gitlab.freedesktop.org/poppler/poppler>)
- **License:** GPL-2.0-only OR GPL-3.0-only
- **Parsed scope:** PDF document page count
- **Underlying family:** Poppler PDF parser, GLib C frontend
- **Local input API:** `g_file_get_contents(local path) to GBytes; poppler_document_new_from_bytes(GBytes*, ...); poppler_document_get_n_pages()`
- **Documentation:** [API reference](<https://poppler.freedesktop.org/api/glib/PopplerDocument.html>)
- **Catalog evidence:** [parser record](../../../../data/c/pdf/parsers.json) · [control verification](../../../../data/c/pdf/verification.json) · [within-ecosystem ranking](../../../../data/c/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

Poppler GLib C API shares core parser with the C++ Poppler frontend in the C++ PDF cell.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/c/poppler-glib/README.md)

```sh
python3 parsarium.py build pdf c poppler-glib
python3 parsarium.py run pdf c poppler-glib controls/pdf/one-page.pdf
```
