# icepdf-core — PDF / Java

Pinned release: `6.2.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/java/icepdf-core/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf java icepdf_core
python3 parsarium.py run pdf java icepdf_core controls/pdf/one-page.pdf
python3 parsarium.py replay pdf java icepdf_core CORPUS_DIR runs/pdf-icepdf_core-replay
python3 parsarium.py afl build pdf java icepdf_core
python3 parsarium.py afl prepare pdf java icepdf_core runs/pdf-icepdf_core-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
