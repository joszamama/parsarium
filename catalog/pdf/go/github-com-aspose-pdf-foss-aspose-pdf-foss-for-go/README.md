# github.com/aspose-pdf-foss/aspose-pdf-foss-for-go — PDF / Go

- **Pinned release:** `v0.16.0`
- **License:** MIT
- **Parsed scope:** page count
- **Underlying family:** Aspose PDF FOSS
- **Local input API:** `OpenStream(io.Reader).PageCount()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/aspose-pdf-foss/aspose-pdf-foss-for-go@v0.16.0>)
- **Catalog evidence:** [parser record](../../../../data/go/pdf/parsers.json) · [control verification](../../../../data/go/pdf/verification.json) · [within-ecosystem ranking](../../../../data/go/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/go/github_com_aspose_pdf_foss_aspose_pdf_foss_for_go/README.md)

```sh
python3 parsarium.py build pdf go github_com_aspose_pdf_foss_aspose_pdf_foss_for_go
python3 parsarium.py run pdf go github_com_aspose_pdf_foss_aspose_pdf_foss_for_go controls/pdf/one-page.pdf
```
