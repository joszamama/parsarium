# gitee.com/leijacob/pdf — PDF / Go

- **Pinned release:** `v1.1.7`
- **License:** BSD-3-Clause
- **Parsed scope:** page count
- **Underlying family:** rsc PDF reader lineage
- **Local input API:** `NewReader(io.ReaderAt, size).NumPage()`
- **Documentation:** [API reference](<https://pkg.go.dev/gitee.com/leijacob/pdf@v1.1.7>)
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

[Docker harness and verification receipt](../../../../projects/pdf/go/gitee_com_leijacob_pdf/README.md)

```sh
python3 parsarium.py build pdf go gitee_com_leijacob_pdf
python3 parsarium.py run pdf go gitee_com_leijacob_pdf controls/pdf/one-page.pdf
```
