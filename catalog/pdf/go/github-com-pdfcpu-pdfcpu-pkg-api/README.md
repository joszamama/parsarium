# github.com/pdfcpu/pdfcpu/pkg/api — PDF / Go

- **Pinned release:** `v0.16.4`
- **License:** Apache-2.0
- **Parsed scope:** page count
- **Underlying family:** pdfcpu PDF processor
- **Local input API:** `PageCount(context.Context, io.ReadSeeker, nil)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/pdfcpu/pdfcpu/pkg/api@v0.16.4>)
- **Catalog evidence:** [parser record](../../../../data/go/pdf/parsers.json) · [control verification](../../../../data/go/pdf/verification.json) · [within-ecosystem ranking](../../../../data/go/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/go/github_com_pdfcpu_pdfcpu_pkg_api/README.md)

```sh
python3 parsarium.py build pdf go github_com_pdfcpu_pdfcpu_pkg_api
python3 parsarium.py run pdf go github_com_pdfcpu_pdfcpu_pkg_api controls/pdf/one-page.pdf
```
