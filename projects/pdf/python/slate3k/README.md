# slate3k — PDF / Python

Pinned release: `0.5.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/python/slate3k/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf python slate3k
python3 parsarium.py run pdf python slate3k controls/pdf/one-page.pdf
python3 parsarium.py replay pdf python slate3k CORPUS_DIR runs/pdf-slate3k-replay
python3 parsarium.py afl build pdf python slate3k
python3 parsarium.py afl prepare pdf python slate3k runs/pdf-slate3k-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
