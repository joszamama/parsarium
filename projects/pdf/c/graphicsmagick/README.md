# graphicsmagick — PDF / C

Pinned release: `1.3.49`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/c/graphicsmagick/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf c graphicsmagick
python3 parsarium.py run pdf c graphicsmagick controls/pdf/one-page.pdf
python3 parsarium.py replay pdf c graphicsmagick CORPUS_DIR runs/pdf-graphicsmagick-replay
python3 parsarium.py afl build pdf c graphicsmagick
python3 parsarium.py afl prepare pdf c graphicsmagick runs/pdf-graphicsmagick-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
