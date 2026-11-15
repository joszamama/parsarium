# smalot/pdfparser — PDF / PHP

- **Pinned release:** `v2.13.1`
- **License:** LGPL-3.0
- **Parsed scope:** One PDF page and embedded Parsarium text
- **Underlying family:** Smalot native PHP PDF parser
- **Local input API:** `Parser::parseFile(local PDF path); page count and extracted text`
- **Documentation:** [API reference](<https://github.com/smalot/pdfparser/blob/a71c6dd38e60a995fdb4d36e4433b8b3557c65dc/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/pdf/parsers.json) · [control verification](../../../../data/php/pdf/verification.json) · [within-ecosystem ranking](../../../../data/php/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1,
  "text": "Parsarium"
}
```

Own PHP PDF object and content stream parser.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
