# github.com/pdfcpu/pdfcpu/pkg/api — PDF / Go

Pinned release: `v0.16.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/go/github-com-pdfcpu-pdfcpu-pkg-api/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf go github_com_pdfcpu_pdfcpu_pkg_api
python3 parsarium.py run pdf go github_com_pdfcpu_pdfcpu_pkg_api controls/pdf/one-page.pdf
python3 parsarium.py replay pdf go github_com_pdfcpu_pdfcpu_pkg_api CORPUS_DIR runs/pdf-github_com_pdfcpu_pdfcpu_pkg_api-replay
python3 parsarium.py afl build pdf go github_com_pdfcpu_pdfcpu_pkg_api
python3 parsarium.py afl prepare pdf go github_com_pdfcpu_pdfcpu_pkg_api runs/pdf-github_com_pdfcpu_pdfcpu_pkg_api-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
