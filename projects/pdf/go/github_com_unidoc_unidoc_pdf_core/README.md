# github.com/unidoc/unidoc/pdf/core — PDF / Go

Pinned release: `v2.2.0+incompatible`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/go/github-com-unidoc-unidoc-pdf-core/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf go github_com_unidoc_unidoc_pdf_core
python3 parsarium.py run pdf go github_com_unidoc_unidoc_pdf_core controls/pdf/one-page.pdf
python3 parsarium.py replay pdf go github_com_unidoc_unidoc_pdf_core CORPUS_DIR runs/pdf-github_com_unidoc_unidoc_pdf_core-replay
python3 parsarium.py afl build pdf go github_com_unidoc_unidoc_pdf_core
python3 parsarium.py afl prepare pdf go github_com_unidoc_unidoc_pdf_core runs/pdf-github_com_unidoc_unidoc_pdf_core-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
