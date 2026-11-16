# svg-salamander — SVG / Java

Pinned release: `1.1.5.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/java/svg-salamander/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg java svg_salamander
python3 parsarium.py run svg java svg_salamander controls/svg/red-green.svg
python3 parsarium.py replay svg java svg_salamander CORPUS_DIR runs/svg-svg_salamander-replay
python3 parsarium.py afl build svg java svg_salamander
python3 parsarium.py afl prepare svg java svg_salamander runs/svg-svg_salamander-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
