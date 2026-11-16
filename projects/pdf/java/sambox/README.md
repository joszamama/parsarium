# sambox — PDF / Java

Pinned release: `4.0.0.M8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/java/sambox/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf java sambox
python3 parsarium.py run pdf java sambox controls/pdf/one-page.pdf
python3 parsarium.py replay pdf java sambox CORPUS_DIR runs/pdf-sambox-replay
python3 parsarium.py afl build pdf java sambox
python3 parsarium.py afl prepare pdf java sambox runs/pdf-sambox-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
