# seehuhn.de/go/pdf — PDF / Go

- **Pinned release:** `v0.8.0`
- **License:** BSD-3-Clause
- **Parsed scope:** PDF version
- **Underlying family:** seehuhn PDF reader
- **Local input API:** `NewReader(io.ReaderAt, size, nil).GetMeta().Version`
- **Documentation:** [API reference](<https://pkg.go.dev/seehuhn.de/go/pdf@v0.8.0>)
- **Catalog evidence:** [parser record](../../../../data/go/pdf/parsers.json) · [control verification](../../../../data/go/pdf/verification.json) · [within-ecosystem ranking](../../../../data/go/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "version": "1.4"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/go/seehuhn_de_go_pdf/README.md)

```sh
python3 parsarium.py build pdf go seehuhn_de_go_pdf
python3 parsarium.py run pdf go seehuhn_de_go_pdf controls/pdf/one-page.pdf
```
