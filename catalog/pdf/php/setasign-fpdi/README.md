# setasign/fpdi — PDF / PHP

- **Pinned release:** `v2.6.10`
- **License:** MIT
- **Parsed scope:** One PDF page, 216 × 279 mm rounded imported MediaBox
- **Underlying family:** FPDI native PHP PDF object reader
- **Local input API:** `Fpdi::setSourceFile(local PDF path), importPage(1), getTemplateSize(); page count and dimensions`
- **Documentation:** [API reference](<https://github.com/Setasign/FPDI/blob/be29a9d43c64f06569c1075f181e43d829a3d5bb/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/pdf/parsers.json) · [control verification](../../../../data/php/pdf/verification.json) · [within-ecosystem ranking](../../../../data/php/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1,
  "width": 216,
  "height": 279
}
```

FPDI reads and imports the PDF page using its own parser; setasign/fpdf 1.9.0 is a required rendering companion, not a separate PDF reader.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/php/fpdi/README.md)

```sh
python3 parsarium.py build pdf php fpdi
python3 parsarium.py run pdf php fpdi controls/pdf/one-page.pdf
```
