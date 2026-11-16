# scireum-jpod — PDF / Java

Pinned release: `2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/java/scireum-jpod/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf java scireum_jpod
python3 parsarium.py run pdf java scireum_jpod controls/pdf/one-page.pdf
python3 parsarium.py replay pdf java scireum_jpod CORPUS_DIR runs/pdf-scireum_jpod-replay
python3 parsarium.py afl build pdf java scireum_jpod
python3 parsarium.py afl prepare pdf java scireum_jpod runs/pdf-scireum_jpod-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
