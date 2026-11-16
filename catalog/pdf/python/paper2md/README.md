# paper2md — PDF / Python

- **Pinned release:** `0.1.0`
- **License:** MIT
- **Parsed scope:** page text as Markdown
- **Underlying family:** paper2md via MuPDF
- **Local input API:** `paper2md.convert(local path)`
- **Documentation:** [API reference](<https://pypi.org/project/paper2md/0.1.0/>)
- **Catalog evidence:** [parser record](../../../../data/python/pdf/parsers.json) · [control verification](../../../../data/python/pdf/verification.json) · [within-ecosystem ranking](../../../../data/python/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "text": "Parsarium"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/python/paper2md/README.md)

```sh
python3 parsarium.py build pdf python paper2md
python3 parsarium.py run pdf python paper2md controls/pdf/one-page.pdf
```
