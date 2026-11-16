# graphicsmagick — PNG / C++

Pinned release: `1.3.49`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/cpp/graphicsmagick/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png cpp graphicsmagick
python3 parsarium.py run png cpp graphicsmagick controls/png/red-green.png
python3 parsarium.py replay png cpp graphicsmagick CORPUS_DIR runs/png-graphicsmagick-replay
python3 parsarium.py afl build png cpp graphicsmagick
python3 parsarium.py afl prepare png cpp graphicsmagick runs/png-graphicsmagick-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
