# podofo — PDF / C++

- **Pinned release:** `1.1.2`
- **Upstream:** [source repository](<https://github.com/podofo/podofo>)
- **License:** LGPL-2.0-or-later OR MPL-2.0
- **Parsed scope:** PDF document page count
- **Underlying family:** PoDoFo PDF parser
- **Local input API:** `PoDoFo::PdfMemDocument::Load(std::string_view local filename); GetPages().GetCount()`
- **Documentation:** [API reference](<https://github.com/podofo/podofo/blob/1.1.2/src/podofo/main/PdfMemDocument.h>)
- **Catalog evidence:** [parser record](../../../../data/cpp/pdf/parsers.json) · [control verification](../../../../data/cpp/pdf/verification.json) · [within-ecosystem ranking](../../../../data/cpp/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

Native C++17 PoDoFo PDF document reader; distinct from Poppler.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/cpp/podofo/README.md)

```sh
python3 parsarium.py build pdf cpp podofo
python3 parsarium.py run pdf cpp podofo controls/pdf/one-page.pdf
```
