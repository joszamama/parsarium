# imagemagick — PDF / C

Pinned release: `7.1.2-35`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/c/imagemagick/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf c imagemagick
python3 parsarium.py run pdf c imagemagick controls/pdf/one-page.pdf
python3 parsarium.py replay pdf c imagemagick CORPUS_DIR runs/pdf-imagemagick-replay
python3 parsarium.py afl build pdf c imagemagick
python3 parsarium.py afl prepare pdf c imagemagick runs/pdf-imagemagick-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
