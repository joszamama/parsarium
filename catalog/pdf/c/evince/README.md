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

The verified Docker control uses Evince's GFile factory on a local PDF. The byte-input AFL harness uses Evince's documented file-descriptor factory. The two loader methods converge at Evince's PDF backend and Poppler GLib/core; this is a package path sharing Poppler's PDF syntax parser, not an independent engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/c/evince/README.md)

```sh
python3 parsarium.py build pdf c evince
python3 parsarium.py run pdf c evince controls/pdf/two-page.pdf
```
