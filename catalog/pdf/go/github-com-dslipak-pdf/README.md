# github.com/dslipak/pdf — PDF / Go

- **Pinned release:** `v0.0.2`
- **Upstream:** [source repository](<https://github.com/dslipak/pdf>) · [pkg.go.dev](<https://pkg.go.dev/github.com/dslipak/pdf>)
- **License:** BSD-3-Clause
- **Parsed scope:** page count
- **Underlying family:** rsc PDF reader lineage
- **Local input API:** `NewReader(io.ReaderAt, size).NumPage()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/dslipak/pdf@v0.0.2>)
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

[Docker harness and verification receipt](../../../../projects/pdf/go/github_com_dslipak_pdf/README.md)

```sh
python3 parsarium.py build pdf go github_com_dslipak_pdf
python3 parsarium.py run pdf go github_com_dslipak_pdf controls/pdf/one-page.pdf
```
