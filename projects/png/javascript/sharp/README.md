# sharp — PNG / JavaScript

Pinned release: `0.35.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/javascript/sharp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png javascript sharp
python3 parsarium.py run png javascript sharp controls/png/red-green.png
python3 parsarium.py replay png javascript sharp CORPUS_DIR runs/png-sharp-replay
python3 parsarium.py afl build png javascript sharp
python3 parsarium.py afl prepare png javascript sharp runs/png-sharp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
