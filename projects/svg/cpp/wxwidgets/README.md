# wxwidgets — SVG / C++

Pinned release: `3.3.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/cpp/wxwidgets/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg cpp wxwidgets
python3 parsarium.py run svg cpp wxwidgets controls/svg/red-green.svg
python3 parsarium.py replay svg cpp wxwidgets CORPUS_DIR runs/svg-wxwidgets-replay
python3 parsarium.py afl build svg cpp wxwidgets
python3 parsarium.py afl prepare svg cpp wxwidgets runs/svg-wxwidgets-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
