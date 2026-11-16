# pypdfium2 — PDF / Python

Pinned release: `5.10.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/python/pypdfium2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf python pypdfium2
python3 parsarium.py run pdf python pypdfium2 controls/pdf/one-page.pdf
python3 parsarium.py replay pdf python pypdfium2 CORPUS_DIR runs/pdf-pypdfium2-replay
python3 parsarium.py afl build pdf python pypdfium2
python3 parsarium.py afl prepare pdf python pypdfium2 runs/pdf-pypdfium2-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
