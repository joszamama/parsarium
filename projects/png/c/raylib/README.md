# raylib — PNG / C

Pinned release: `6.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/c/raylib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png c raylib
python3 parsarium.py run png c raylib controls/png/red-green.png
python3 parsarium.py replay png c raylib CORPUS_DIR runs/png-raylib-replay
python3 parsarium.py afl build png c raylib
python3 parsarium.py afl prepare png c raylib runs/png-raylib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
