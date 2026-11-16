# xmlgraphics-commons — PNG / Java

Pinned release: `2.12`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/java/xmlgraphics-commons/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png java xmlgraphics_commons
python3 parsarium.py run png java xmlgraphics_commons controls/png/red-green.png
python3 parsarium.py replay png java xmlgraphics_commons CORPUS_DIR runs/png-xmlgraphics_commons-replay
python3 parsarium.py afl build png java xmlgraphics_commons
python3 parsarium.py afl prepare png java xmlgraphics_commons runs/png-xmlgraphics_commons-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
