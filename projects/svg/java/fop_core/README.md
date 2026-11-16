# fop-core — SVG / Java

Pinned release: `2.12`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/java/fop-core/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg java fop_core
python3 parsarium.py run svg java fop_core controls/svg/red-green.svg
python3 parsarium.py replay svg java fop_core CORPUS_DIR runs/svg-fop_core-replay
python3 parsarium.py afl build svg java fop_core
python3 parsarium.py afl prepare svg java fop_core runs/svg-fop_core-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
