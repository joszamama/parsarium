# libvips — PDF / C++

Pinned release: `8.18.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/cpp/libvips/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf cpp libvips
python3 parsarium.py run pdf cpp libvips controls/pdf/one-page.pdf
python3 parsarium.py replay pdf cpp libvips CORPUS_DIR runs/pdf-libvips-replay
python3 parsarium.py afl build pdf cpp libvips
python3 parsarium.py afl prepare pdf cpp libvips runs/pdf-libvips-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
