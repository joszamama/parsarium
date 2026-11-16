# tika-pdf — PDF / Java

Pinned release: `4.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/java/tika-pdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf java tika_pdf
python3 parsarium.py run pdf java tika_pdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf java tika_pdf CORPUS_DIR runs/pdf-tika_pdf-replay
python3 parsarium.py afl build pdf java tika_pdf
python3 parsarium.py afl prepare pdf java tika_pdf runs/pdf-tika_pdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
