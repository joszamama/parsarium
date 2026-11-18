# propa/tcpdi — PDF / PHP

- **Pinned release:** `v1.3.5`
- **Upstream:** [source repository](<https://github.com/kulbakin/tcpdi>) · [Packagist](<https://packagist.org/packages/propa/tcpdi>)
- **License:** Apache-2.0
- **Parsed scope:** One PDF page, 216 × 279 mm rounded imported MediaBox
- **Underlying family:** TCPDI FPDI-derived PHP PDF parser
- **Local input API:** `TCPDI::setSourceFile(local PDF path), importPage(1), getTemplateSize(); page count and dimensions`
- **Documentation:** [API reference](<https://github.com/kulbakin/tcpdi/blob/4fec3053f8792e3c546eab62d82f6ce42925169b/README.md>)
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

TCPDI is a separately maintained FPDI-derived import implementation bundled with its own tcpdi_parser; TCPDF is the rendering companion.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/php/propa_tcpdi/README.md)

```sh
python3 parsarium.py build pdf php propa_tcpdi
python3 parsarium.py run pdf php propa_tcpdi controls/pdf/one-page.pdf
```
