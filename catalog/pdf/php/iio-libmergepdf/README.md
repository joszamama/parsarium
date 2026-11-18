# iio/libmergepdf — PDF / PHP

- **Pinned release:** `4.0.4`
- **Upstream:** [source repository](<https://github.com/hanneskod/libmergepdf>) · [Packagist](<https://packagist.org/packages/iio/libmergepdf>)
- **License:** WTFPL
- **Parsed scope:** One imported PDF page object in emitted PDF
- **Underlying family:** FPDI native PHP PDF object reader
- **Local input API:** `Merger::addFile(local PDF path), merge(); imported page object in emitted PDF`
- **Documentation:** [API reference](<https://github.com/hanneskod/libmergepdf/blob/6613b978c08d00d559796ab510614243e4dd5dfb/src/Merger.php>)
- **Catalog evidence:** [parser record](../../../../data/php/pdf/parsers.json) · [control verification](../../../../data/php/pdf/verification.json) · [within-ecosystem ranking](../../../../data/php/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pdf_header": true,
  "page_objects": 1
}
```

Merger wrapper delegates PDF import to pinned FPDI 2.6.10; shared parser family with setasign/fpdi, counted as a separate Composer package path.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/php/iio_libmergepdf/README.md)

```sh
python3 parsarium.py build pdf php iio_libmergepdf
python3 parsarium.py run pdf php iio_libmergepdf controls/pdf/one-page.pdf
```
