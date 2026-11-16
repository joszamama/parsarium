# parse-png — PNG / JavaScript

Pinned release: `2.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/javascript/parse-png/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png javascript parse_png
python3 parsarium.py run png javascript parse_png controls/png/red-green.png
python3 parsarium.py replay png javascript parse_png CORPUS_DIR runs/png-parse_png-replay
python3 parsarium.py afl build png javascript parse_png
python3 parsarium.py afl prepare png javascript parse_png runs/png-parse_png-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
