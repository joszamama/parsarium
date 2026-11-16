# stb — PNG / C++

Pinned release: `cci.20261021`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/cpp/stb/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png cpp stb
python3 parsarium.py run png cpp stb controls/png/red-green.png
python3 parsarium.py replay png cpp stb CORPUS_DIR runs/png-stb-replay
python3 parsarium.py afl build png cpp stb
python3 parsarium.py afl prepare png cpp stb runs/png-stb-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
