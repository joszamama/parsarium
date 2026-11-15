# iio/libmergepdf — PDF / PHP

- **Pinned release:** `4.0.4`
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
