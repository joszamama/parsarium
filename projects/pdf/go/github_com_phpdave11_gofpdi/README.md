# github.com/phpdave11/gofpdi — PDF / Go

Pinned release: `v1.0.16`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/go/github-com-phpdave11-gofpdi/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf go github_com_phpdave11_gofpdi
python3 parsarium.py run pdf go github_com_phpdave11_gofpdi controls/pdf/one-page.pdf
python3 parsarium.py replay pdf go github_com_phpdave11_gofpdi CORPUS_DIR runs/pdf-github_com_phpdave11_gofpdi-replay
python3 parsarium.py afl build pdf go github_com_phpdave11_gofpdi
python3 parsarium.py afl prepare pdf go github_com_phpdave11_gofpdi runs/pdf-github_com_phpdave11_gofpdi-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
