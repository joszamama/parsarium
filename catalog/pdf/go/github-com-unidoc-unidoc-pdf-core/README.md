# github.com/unidoc/unidoc/pdf/core — PDF / Go

- **Pinned release:** `v2.2.0+incompatible`
- **Upstream:** [source repository](<https://github.com/unidoc/unidoc>) · [pkg.go.dev](<https://pkg.go.dev/github.com/unidoc/unidoc/pdf/core>)
- **License:** AGPL-3.0 or commercial (AGPL option used for open-source qualification)
- **Parsed scope:** PDF indirect object count
- **Underlying family:** UniDoc core
- **Local input API:** `NewParser(io.ReadSeeker).GetObjectNums()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/unidoc/unidoc/pdf/core@v2.2.0+incompatible>)
- **Catalog evidence:** [parser record](../../../../data/go/pdf/parsers.json) · [control verification](../../../../data/go/pdf/verification.json) · [within-ecosystem ranking](../../../../data/go/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "objects": 6
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/go/github_com_unidoc_unidoc_pdf_core/README.md)

```sh
python3 parsarium.py build pdf go github_com_unidoc_unidoc_pdf_core
python3 parsarium.py run pdf go github_com_unidoc_unidoc_pdf_core controls/pdf/one-page.pdf
```
