# openpdf-renderer — PDF / Java

Pinned release: `3.0.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/java/openpdf-renderer/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf java openpdf_renderer
python3 parsarium.py run pdf java openpdf_renderer controls/pdf/one-page.pdf
python3 parsarium.py replay pdf java openpdf_renderer CORPUS_DIR runs/pdf-openpdf_renderer-replay
python3 parsarium.py afl build pdf java openpdf_renderer
python3 parsarium.py afl prepare pdf java openpdf_renderer runs/pdf-openpdf_renderer-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
