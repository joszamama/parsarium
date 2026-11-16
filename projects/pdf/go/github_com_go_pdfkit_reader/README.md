# github.com/go-pdfkit/reader — PDF / Go

Pinned release: `v0.10.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/go/github-com-go-pdfkit-reader/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf go github_com_go_pdfkit_reader
python3 parsarium.py run pdf go github_com_go_pdfkit_reader controls/pdf/one-page.pdf
python3 parsarium.py replay pdf go github_com_go_pdfkit_reader CORPUS_DIR runs/pdf-github_com_go_pdfkit_reader-replay
python3 parsarium.py afl build pdf go github_com_go_pdfkit_reader
python3 parsarium.py afl prepare pdf go github_com_go_pdfkit_reader runs/pdf-github_com_go_pdfkit_reader-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
