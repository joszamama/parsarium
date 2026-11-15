# stb — PNG / C

Pinned release: `cci.20261021`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/c/stb/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png c stb
python3 parsarium.py run png c stb controls/png/red-green.png
python3 parsarium.py replay png c stb CORPUS_DIR runs/png-stb-replay
python3 parsarium.py afl build png c stb
python3 parsarium.py afl prepare png c stb runs/png-stb-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
