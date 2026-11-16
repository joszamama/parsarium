# prinsfrank/pdfparser — PDF / PHP

- **Pinned release:** `v4.3.0`
- **License:** MIT
- **Parsed scope:** Embedded Parsarium text extracted from PDF
- **Underlying family:** PrinsFrank native PHP PDF parser
- **Local input API:** `PdfParser::parseFile(local PDF path)->getText()`
- **Documentation:** [API reference](<https://github.com/PrinsFrank/pdfparser/blob/441e0669b61e4028ba34c030d6625770c8f7e1ad/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/pdf/parsers.json) · [control verification](../../../../data/php/pdf/verification.json) · [within-ecosystem ranking](../../../../data/php/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "text": "Parsarium"
}
```

Own PHP PDF object and content stream parser.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/php/prinsfrank_pdfparser/README.md)

```sh
python3 parsarium.py build pdf php prinsfrank_pdfparser
python3 parsarium.py run pdf php prinsfrank_pdfparser controls/pdf/one-page.pdf
```
