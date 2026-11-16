# imgio — PNG / Python

Pinned release: `1.7.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/python/imgio/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png python imgio
python3 parsarium.py run png python imgio controls/png/red-green.png
python3 parsarium.py replay png python imgio CORPUS_DIR runs/png-imgio-replay
python3 parsarium.py afl build png python imgio
python3 parsarium.py afl prepare png python imgio runs/png-imgio-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
