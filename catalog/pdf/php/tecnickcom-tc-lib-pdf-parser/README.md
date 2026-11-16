# tecnickcom/tc-lib-pdf-parser — PDF / PHP

- **Pinned release:** `3.16.7`
- **License:** LGPL-3.0-or-later
- **Parsed scope:** Six indirect PDF objects and parsed cross-reference structure
- **Underlying family:** TCPDF parser native PHP PDF object reader
- **Local input API:** `Parser::parse(local PDF bytes); cross-reference array and decoded object count`
- **Documentation:** [API reference](<https://github.com/tecnickcom/tc-lib-pdf-parser/blob/f83cadbc3b347732ed928cd7b654589688812c5f/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/pdf/parsers.json) · [control verification](../../../../data/php/pdf/verification.json) · [within-ecosystem ranking](../../../../data/php/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "objects": 6,
  "xref_type": "array"
}
```

Standalone PDF parser package; tc-lib-pdf-filter 2.11.9 is its pinned stream filter dependency.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/php/tecnickcom_tc_lib_pdf_parser/README.md)

```sh
python3 parsarium.py build pdf php tecnickcom_tc_lib_pdf_parser
python3 parsarium.py run pdf php tecnickcom_tc_lib_pdf_parser controls/pdf/one-page.pdf
```
