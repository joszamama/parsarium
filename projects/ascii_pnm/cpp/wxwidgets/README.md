# wxwidgets — ASCII PNM / C++

Pinned release: `3.3.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/cpp/wxwidgets/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm cpp wxwidgets
python3 parsarium.py run ascii_pnm cpp wxwidgets controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm cpp wxwidgets CORPUS_DIR runs/ascii_pnm-wxwidgets-replay
python3 parsarium.py afl build ascii_pnm cpp wxwidgets
python3 parsarium.py afl prepare ascii_pnm cpp wxwidgets runs/ascii_pnm-wxwidgets-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
