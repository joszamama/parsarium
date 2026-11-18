# mikehaertl/php-pdftk — PDF / PHP

- **Pinned release:** `0.14.4`
- **Upstream:** [source repository](<https://github.com/mikehaertl/php-pdftk>) · [Packagist](<https://packagist.org/packages/mikehaertl/php-pdftk>)
- **License:** MIT
- **Parsed scope:** One PDF page and document title
- **Underlying family:** pdftk-java PDF parser
- **Local input API:** `Pdf(local PDF path)->getData(); parsed page count and Title metadata`
- **Documentation:** [API reference](<https://github.com/mikehaertl/php-pdftk/blob/9a88810285c1a26459b67a50e30af51eccc57a9e/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/pdf/parsers.json) · [control verification](../../../../data/php/pdf/verification.json) · [within-ecosystem ranking](../../../../data/php/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1,
  "title": "Parsarium PDF control"
}
```

PHP wrapper invokes pinned local pdftk-java 3.3.3; the native PDF reader is shared with other pdftk wrappers.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/php/mikehaertl_php_pdftk/README.md)

```sh
python3 parsarium.py build pdf php mikehaertl_php_pdftk
python3 parsarium.py run pdf php mikehaertl_php_pdftk controls/pdf/one-page.pdf
```
