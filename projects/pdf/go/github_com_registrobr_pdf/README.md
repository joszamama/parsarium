# github.com/registrobr/pdf — PDF / Go

Pinned release: `v0.2.9`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/go/github-com-registrobr-pdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf go github_com_registrobr_pdf
python3 parsarium.py run pdf go github_com_registrobr_pdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf go github_com_registrobr_pdf CORPUS_DIR runs/pdf-github_com_registrobr_pdf-replay
python3 parsarium.py afl build pdf go github_com_registrobr_pdf
python3 parsarium.py afl prepare pdf go github_com_registrobr_pdf runs/pdf-github_com_registrobr_pdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
