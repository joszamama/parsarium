# pdfminer.six — PDF / Python

- **Pinned release:** `20260107`
- **Upstream:** [source repository](<https://github.com/pdfminer/pdfminer.six>) · [PyPI](<https://pypi.org/project/pdfminer.six/>)
- **License:** MIT
- **Parsed scope:** page text
- **Underlying family:** pdfminer.six
- **Local input API:** `pdfminer.high_level.extract_text(local path)`
- **Documentation:** [API reference](<https://pdfminersix.readthedocs.io/en/latest/tutorial/highlevel.html>)
- **Catalog evidence:** [parser record](../../../../data/python/pdf/parsers.json) · [control verification](../../../../data/python/pdf/verification.json) · [within-ecosystem ranking](../../../../data/python/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "text": "Parsarium"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/python/pdfminer_six/README.md)

```sh
python3 parsarium.py build pdf python pdfminer_six
python3 parsarium.py run pdf python pdfminer_six controls/pdf/one-page.pdf
```
