# ghostscript — PDF / C

- **Pinned release:** `10.08.0`
- **License:** AGPL-3.0-or-later
- **Parsed scope:** PDF interpreter NumPages metadata
- **Underlying family:** Ghostscript PDF interpreter
- **Local input API:** `gsapi_run_string using .PDFInit, local .PDFFile, .PDFInfo /NumPages; file-read permission granted for supplied path`
- **Documentation:** [API reference](<https://ghostscript.readthedocs.io/en/master/Language.html>)
- **Catalog evidence:** [parser record](../../../../data/c/pdf/parsers.json) · [control verification](../../../../data/c/pdf/verification.json) · [within-ecosystem ranking](../../../../data/c/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

Direct Ghostscript C API; same engine and release as C++ PDF call site.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/c/ghostscript/README.md)

```sh
python3 parsarium.py build pdf c ghostscript
python3 parsarium.py run pdf c ghostscript controls/pdf/one-page.pdf
```
