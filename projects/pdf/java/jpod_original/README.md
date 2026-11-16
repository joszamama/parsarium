# jpod-original — PDF / Java

Pinned release: `5.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/java/jpod-original/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf java jpod_original
python3 parsarium.py run pdf java jpod_original controls/pdf/one-page.pdf
python3 parsarium.py replay pdf java jpod_original CORPUS_DIR runs/pdf-jpod_original-replay
python3 parsarium.py afl build pdf java jpod_original
python3 parsarium.py afl prepare pdf java jpod_original runs/pdf-jpod_original-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
