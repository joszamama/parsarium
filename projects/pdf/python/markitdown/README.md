# markitdown — PDF / Python

Pinned release: `0.1.9`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/python/markitdown/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf python markitdown
python3 parsarium.py run pdf python markitdown controls/pdf/one-page.pdf
python3 parsarium.py replay pdf python markitdown CORPUS_DIR runs/pdf-markitdown-replay
python3 parsarium.py afl build pdf python markitdown
python3 parsarium.py afl prepare pdf python markitdown runs/pdf-markitdown-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
