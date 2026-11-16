# raylib — PNG / C++

Pinned release: `6.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/cpp/raylib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png cpp raylib
python3 parsarium.py run png cpp raylib controls/png/red-green.png
python3 parsarium.py replay png cpp raylib CORPUS_DIR runs/png-raylib-replay
python3 parsarium.py afl build png cpp raylib
python3 parsarium.py afl prepare png cpp raylib runs/png-raylib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
