# jSVGIcon — SVG / Java

Pinned release: `1.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/java/jsvgicon/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg java jsvgicon
python3 parsarium.py run svg java jsvgicon controls/svg/red-green.svg
python3 parsarium.py replay svg java jsvgicon CORPUS_DIR runs/svg-jsvgicon-replay
python3 parsarium.py afl build svg java jsvgicon
python3 parsarium.py afl prepare svg java jsvgicon runs/svg-jsvgicon-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
