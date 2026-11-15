# pngj — PNG / Java

Pinned release: `2.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/java/pngj/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png java pngj
python3 parsarium.py run png java pngj controls/png/red-green.png
python3 parsarium.py replay png java pngj CORPUS_DIR runs/png-pngj-replay
python3 parsarium.py afl build png java pngj
python3 parsarium.py afl prepare png java pngj runs/png-pngj-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
