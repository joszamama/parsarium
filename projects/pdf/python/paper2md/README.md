# paper2md — PDF / Python

Pinned release: `0.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/python/paper2md/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf python paper2md
python3 parsarium.py run pdf python paper2md controls/pdf/one-page.pdf
python3 parsarium.py replay pdf python paper2md CORPUS_DIR runs/pdf-paper2md-replay
python3 parsarium.py afl build pdf python paper2md
python3 parsarium.py afl prepare pdf python paper2md runs/pdf-paper2md-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
