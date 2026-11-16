# github.com/benoitkugler/pdf/reader — PDF / Go

- **Pinned release:** `v0.0.15`
- **License:** MIT
- **Parsed scope:** page count
- **Underlying family:** benoitkugler PDF model
- **Local input API:** `ParsePDFReader(io.ReadSeeker, Options{}).Catalog.Pages.Count()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/benoitkugler/pdf/reader@v0.0.15>)
- **Catalog evidence:** [parser record](../../../../data/go/pdf/parsers.json) · [control verification](../../../../data/go/pdf/verification.json) · [within-ecosystem ranking](../../../../data/go/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/go/github_com_benoitkugler_pdf_reader/README.md)

```sh
python3 parsarium.py build pdf go github_com_benoitkugler_pdf_reader
python3 parsarium.py run pdf go github_com_benoitkugler_pdf_reader controls/pdf/one-page.pdf
```
