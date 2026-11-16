# imlib2 — SVG / C

Pinned release: `1.12.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/c/imlib2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg c imlib2
python3 parsarium.py run svg c imlib2 controls/svg/red-green.svg
python3 parsarium.py replay svg c imlib2 CORPUS_DIR runs/svg-imlib2-replay
python3 parsarium.py afl build svg c imlib2
python3 parsarium.py afl prepare svg c imlib2 runs/svg-imlib2-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
