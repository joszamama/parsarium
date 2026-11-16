# jpdfium — PDF / Java

Pinned release: `1.3.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/java/jpdfium/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf java jpdfium
python3 parsarium.py run pdf java jpdfium controls/pdf/one-page.pdf
python3 parsarium.py replay pdf java jpdfium CORPUS_DIR runs/pdf-jpdfium-replay
python3 parsarium.py afl build pdf java jpdfium
python3 parsarium.py afl prepare pdf java jpdfium runs/pdf-jpdfium-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
