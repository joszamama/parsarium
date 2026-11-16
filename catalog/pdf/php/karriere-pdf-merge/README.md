# karriere/pdf-merge — PDF / PHP

- **Pinned release:** `v3.4.0`
- **License:** Apache-2.0
- **Parsed scope:** One imported page object in emitted PDF
- **Underlying family:** TCPDI FPDI-derived PHP PDF parser
- **Local input API:** `PdfMerge::add(local PDF path), merge(string); one imported PDF page object`
- **Documentation:** [API reference](<https://github.com/karriereat/pdf-merge/blob/13e6f60fe42c0fac238a65b9e19d69875658379b/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/pdf/parsers.json) · [control verification](../../../../data/php/pdf/verification.json) · [within-ecosystem ranking](../../../../data/php/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pdf_header": true,
  "page_objects": 1
}
```

Wrapper bundles a TCPDI parser derived from FPDI and uses pinned TCPDF 6.11.4 as rendering companion.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/php/karriere_pdf_merge/README.md)

```sh
python3 parsarium.py build pdf php karriere_pdf_merge
python3 parsarium.py run pdf php karriere_pdf_merge controls/pdf/one-page.pdf
```
