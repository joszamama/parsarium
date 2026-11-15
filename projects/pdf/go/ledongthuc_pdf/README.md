# github.com/ledongthuc/pdf — PDF / Go

Pinned release: `v0.0.0-20261020125853-5e46805f718e`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/go/github-com-ledongthuc-pdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf go ledongthuc_pdf
python3 parsarium.py run pdf go ledongthuc_pdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf go ledongthuc_pdf CORPUS_DIR runs/pdf-ledongthuc_pdf-replay
python3 parsarium.py afl build pdf go ledongthuc_pdf
python3 parsarium.py afl prepare pdf go ledongthuc_pdf runs/pdf-ledongthuc_pdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
