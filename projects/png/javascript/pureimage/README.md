# pureimage — PNG / JavaScript

Pinned release: `0.4.20`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/javascript/pureimage/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png javascript pureimage
python3 parsarium.py run png javascript pureimage controls/png/red-green.png
python3 parsarium.py replay png javascript pureimage CORPUS_DIR runs/png-pureimage-replay
python3 parsarium.py afl build png javascript pureimage
python3 parsarium.py afl prepare png javascript pureimage runs/png-pureimage-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
