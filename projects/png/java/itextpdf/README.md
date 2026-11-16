# itextpdf — PNG / Java

Pinned release: `5.5.13`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/java/itextpdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png java itextpdf
python3 parsarium.py run png java itextpdf controls/png/red-green.png
python3 parsarium.py replay png java itextpdf CORPUS_DIR runs/png-itextpdf-replay
python3 parsarium.py afl build png java itextpdf
python3 parsarium.py afl prepare png java itextpdf runs/png-itextpdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
