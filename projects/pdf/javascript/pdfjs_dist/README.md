# pdfjs-dist — PDF / JavaScript

Pinned release: `6.5.438`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/javascript/pdfjs-dist/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf javascript pdfjs_dist
python3 parsarium.py run pdf javascript pdfjs_dist controls/pdf/one-page.pdf
python3 parsarium.py replay pdf javascript pdfjs_dist CORPUS_DIR runs/pdf-pdfjs_dist-replay
python3 parsarium.py afl build pdf javascript pdfjs_dist
python3 parsarium.py afl prepare pdf javascript pdfjs_dist runs/pdf-pdfjs_dist-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
