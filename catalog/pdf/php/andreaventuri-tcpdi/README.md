# andreaventuri/tcpdi — PDF / PHP

- **Pinned release:** `1.0.6`
- **License:** Apache-2.0
- **Parsed scope:** One PDF page, 216 × 279 mm rounded imported MediaBox
- **Underlying family:** TCPDI FPDI-derived PHP PDF parser
- **Local input API:** `TCPDI::setSourceFile(local PDF path), importPage(1), getTemplateSize(); page count and dimensions`
- **Documentation:** [API reference](<https://github.com/andreaventuri/tcpdi/blob/b85b4a1aa02823917285d0c46595282abdbb5ac3/README.md>)
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

Separately packaged TCPDI fork; TCPDF 6.11.4 is pinned as companion because its open-ended constraint selected incompatible TCPDF 7. PHP 8.5 emits a deprecation and parser warning while still returning the expected valid-control result.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/php/andreaventuri_tcpdi/README.md)

```sh
python3 parsarium.py build pdf php andreaventuri_tcpdi
python3 parsarium.py run pdf php andreaventuri_tcpdi controls/pdf/one-page.pdf
```
