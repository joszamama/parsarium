# cimg — ASCII PNM / C++

Pinned release: `4.0.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/cpp/cimg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm cpp cimg
python3 parsarium.py run ascii_pnm cpp cimg controls/ascii_pnm/red-green-inline.ppm
python3 parsarium.py replay ascii_pnm cpp cimg CORPUS_DIR runs/ascii_pnm-cimg-replay
python3 parsarium.py afl build ascii_pnm cpp cimg
python3 parsarium.py afl prepare ascii_pnm cpp cimg runs/ascii_pnm-cimg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
