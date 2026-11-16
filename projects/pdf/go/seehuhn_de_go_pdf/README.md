# seehuhn.de/go/pdf — PDF / Go

Pinned release: `v0.8.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/go/seehuhn-de-go-pdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf go seehuhn_de_go_pdf
python3 parsarium.py run pdf go seehuhn_de_go_pdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf go seehuhn_de_go_pdf CORPUS_DIR runs/pdf-seehuhn_de_go_pdf-replay
python3 parsarium.py afl build pdf go seehuhn_de_go_pdf
python3 parsarium.py afl prepare pdf go seehuhn_de_go_pdf runs/pdf-seehuhn_de_go_pdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
