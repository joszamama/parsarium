# pdftext — PDF / Python

- **Pinned release:** `0.7.1`
- **License:** Apache-2.0
- **Parsed scope:** page text
- **Underlying family:** pdftext via PDFium/pypdfium2
- **Local input API:** `pdftext.extraction.plain_text_output(local path)`
- **Documentation:** [API reference](<https://pypi.org/project/pdftext/0.7.1/>)
- **Catalog evidence:** [parser record](../../../../data/python/pdf/parsers.json) · [control verification](../../../../data/python/pdf/verification.json) · [within-ecosystem ranking](../../../../data/python/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "text": "Parsarium"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/python/pdftext/README.md)

```sh
python3 parsarium.py build pdf python pdftext
python3 parsarium.py run pdf python pdftext controls/pdf/one-page.pdf
```
