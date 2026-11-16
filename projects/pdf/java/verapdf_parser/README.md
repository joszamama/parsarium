# verapdf-parser — PDF / Java

Pinned release: `1.30.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/java/verapdf-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf java verapdf_parser
python3 parsarium.py run pdf java verapdf_parser controls/pdf/one-page.pdf
python3 parsarium.py replay pdf java verapdf_parser CORPUS_DIR runs/pdf-verapdf_parser-replay
python3 parsarium.py afl build pdf java verapdf_parser
python3 parsarium.py afl prepare pdf java verapdf_parser runs/pdf-verapdf_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
