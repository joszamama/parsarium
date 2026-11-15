# github.com/srwiley/oksvg — SVG / Go

Pinned release: `v0.0.0-20221011165216-be6e8873101c`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/go/github-com-srwiley-oksvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg go oksvg
python3 parsarium.py run svg go oksvg controls/svg/red-green.svg
python3 parsarium.py replay svg go oksvg CORPUS_DIR runs/svg-oksvg-replay
python3 parsarium.py afl build svg go oksvg
python3 parsarium.py afl prepare svg go oksvg runs/svg-oksvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
