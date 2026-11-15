# rafikhaceb/tcpdi — PDF / PHP

- **Pinned release:** `2.0.3`
- **License:** Apache-2.0
- **Parsed scope:** One PDF page, 216 × 279 mm rounded imported MediaBox
- **Underlying family:** TCPDI FPDI-derived PHP PDF parser
- **Local input API:** `TCPDI::setSourceFile(local PDF path), importPage(1), getTemplateSize(); page count and dimensions`
- **Documentation:** [API reference](<https://github.com/RafikHaceb/tcpdi/blob/ff0ef413c94196247b2c36ff328aacf41ac3e586/README.md>)
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

Separately packaged TCPDI fork with bundled parser; shares the FPDI-derived TCPDI family with propa/tcpdi.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
