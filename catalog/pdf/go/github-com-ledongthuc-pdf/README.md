# github.com/ledongthuc/pdf — PDF / Go

- **Pinned release:** `v0.0.0-20261020125853-5e46805f718e`
- **Upstream:** [source repository](<https://github.com/ledongthuc/pdf>) · [pkg.go.dev](<https://pkg.go.dev/github.com/ledongthuc/pdf>)
- **License:** BSD-3-Clause
- **Parsed scope:** page count
- **Underlying family:** rsc PDF reader lineage
- **Local input API:** `NewReader(io.ReaderAt, size).NumPage()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/ledongthuc/pdf@v0.0.0-20261020125853-5e46805f718e>)
- **Catalog evidence:** [parser record](../../../../data/go/pdf/parsers.json) · [control verification](../../../../data/go/pdf/verification.json) · [within-ecosystem ranking](../../../../data/go/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

Shared code lineage; package count does not imply independent parser engines.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/go/ledongthuc_pdf/README.md)

```sh
python3 parsarium.py build pdf go ledongthuc_pdf
python3 parsarium.py run pdf go ledongthuc_pdf controls/pdf/one-page.pdf
```
