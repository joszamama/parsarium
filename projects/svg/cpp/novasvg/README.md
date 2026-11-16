# novasvg — SVG / C++

Pinned release: `0.11.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/cpp/novasvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg cpp novasvg
python3 parsarium.py run svg cpp novasvg controls/svg/red-green.svg
python3 parsarium.py replay svg cpp novasvg CORPUS_DIR runs/svg-novasvg-replay
python3 parsarium.py afl build svg cpp novasvg
python3 parsarium.py afl prepare svg cpp novasvg runs/svg-novasvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
