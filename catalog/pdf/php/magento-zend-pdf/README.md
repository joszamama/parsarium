# magento/zend-pdf — PDF / PHP

- **Pinned release:** `1.16.7`
- **License:** BSD-3-Clause
- **Parsed scope:** One PDF page and document title
- **Underlying family:** Zend PDF native PHP parser
- **Local input API:** `Zend_Pdf::load(local PDF path); parsed pages and Title metadata`
- **Documentation:** [API reference](<https://github.com/magento/magento-zend-pdf/blob/3c1bc0e69c15666c29b202c37e0bd5897f4db69e/library/Zend/Pdf.php>)
- **Catalog evidence:** [parser record](../../../../data/php/pdf/parsers.json) · [control verification](../../../../data/php/pdf/verification.json) · [within-ecosystem ranking](../../../../data/php/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1,
  "title": "Parsarium PDF control"
}
```

Magento package contains the Zend Framework PDF object reader; its own local file load method parses page and document metadata.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/php/magento_zend_pdf/README.md)

```sh
python3 parsarium.py build pdf php magento_zend_pdf
python3 parsarium.py run pdf php magento_zend_pdf controls/pdf/one-page.pdf
```
