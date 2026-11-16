# goki.dev/svg — SVG / Go

Pinned release: `v0.1.28`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/go/goki-dev-svg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg go goki_dev_svg
python3 parsarium.py run svg go goki_dev_svg controls/svg/red-green.svg
python3 parsarium.py replay svg go goki_dev_svg CORPUS_DIR runs/svg-goki_dev_svg-replay
python3 parsarium.py afl build svg go goki_dev_svg
python3 parsarium.py afl prepare svg go goki_dev_svg runs/svg-goki_dev_svg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
