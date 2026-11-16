# github.com/phpdave11/gofpdi — PDF / Go

- **Pinned release:** `v1.0.16`
- **License:** MIT
- **Parsed scope:** page count
- **Underlying family:** gofpdi importer
- **Local input API:** `NewImporter().SetSourceStream(*io.ReadSeeker).GetNumPages()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/phpdave11/gofpdi@v1.0.16>)
- **Catalog evidence:** [parser record](../../../../data/go/pdf/parsers.json) · [control verification](../../../../data/go/pdf/verification.json) · [within-ecosystem ranking](../../../../data/go/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/go/github_com_phpdave11_gofpdi/README.md)

```sh
python3 parsarium.py build pdf go github_com_phpdave11_gofpdi
python3 parsarium.py run pdf go github_com_phpdave11_gofpdi controls/pdf/one-page.pdf
```
