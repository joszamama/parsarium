# libvips — PDF / C

Pinned release: `8.18.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/c/libvips/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf c libvips
python3 parsarium.py run pdf c libvips controls/pdf/one-page.pdf
python3 parsarium.py replay pdf c libvips CORPUS_DIR runs/pdf-libvips-replay
python3 parsarium.py afl build pdf c libvips
python3 parsarium.py afl prepare pdf c libvips runs/pdf-libvips-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
