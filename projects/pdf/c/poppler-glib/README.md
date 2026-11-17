# poppler-glib — PDF / C

Pinned release: `26.11.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/c/poppler-glib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf c poppler-glib
python3 parsarium.py run pdf c poppler-glib controls/pdf/one-page.pdf
python3 parsarium.py replay pdf c poppler-glib CORPUS_DIR runs/pdf-poppler-glib-replay
python3 parsarium.py afl build pdf c poppler-glib
python3 parsarium.py afl prepare pdf c poppler-glib runs/pdf-poppler-glib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
