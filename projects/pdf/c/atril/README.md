# atril — PDF / C

Pinned release: `1.28.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/c/atril/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf c atril
python3 parsarium.py run pdf c atril controls/pdf/two-page.pdf
python3 parsarium.py replay pdf c atril CORPUS_DIR runs/pdf-atril-replay
python3 parsarium.py afl build pdf c atril
python3 parsarium.py afl prepare pdf c atril runs/pdf-atril-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
