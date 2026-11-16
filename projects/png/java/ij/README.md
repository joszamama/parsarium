# ij — PNG / Java

Pinned release: `1.54p`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/java/ij/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png java ij
python3 parsarium.py run png java ij controls/png/red-green.png
python3 parsarium.py replay png java ij CORPUS_DIR runs/png-ij-replay
python3 parsarium.py afl build png java ij
python3 parsarium.py afl prepare png java ij runs/png-ij-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
