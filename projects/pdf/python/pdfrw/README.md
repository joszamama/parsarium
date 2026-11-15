# pdfrw — PDF / Python

Pinned release: `0.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/python/pdfrw/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf python pdfrw
python3 parsarium.py run pdf python pdfrw controls/pdf/one-page.pdf
python3 parsarium.py replay pdf python pdfrw CORPUS_DIR runs/pdf-pdfrw-replay
python3 parsarium.py afl build pdf python pdfrw
python3 parsarium.py afl prepare pdf python pdfrw runs/pdf-pdfrw-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
