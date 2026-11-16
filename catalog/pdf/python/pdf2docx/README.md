# pdf2docx — PDF / Python

- **Pinned release:** `0.5.13`
- **License:** MIT
- **Parsed scope:** parsed page sections
- **Underlying family:** pdf2docx layout over MuPDF
- **Local input API:** `pdf2docx.Converter(local path).parse()`
- **Documentation:** [API reference](<https://github.com/ArtifexSoftware/pdf2docx/blob/master/pdf2docx/converter.py>)
- **Catalog evidence:** [parser record](../../../../data/python/pdf/parsers.json) · [control verification](../../../../data/python/pdf/verification.json) · [within-ecosystem ranking](../../../../data/python/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1,
  "parsed_sections": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/python/pdf2docx/README.md)

```sh
python3 parsarium.py build pdf python pdf2docx
python3 parsarium.py run pdf python pdf2docx controls/pdf/one-page.pdf
```
