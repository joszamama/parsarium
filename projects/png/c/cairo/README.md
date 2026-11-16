# cairo — PNG / C

Pinned release: `1.18.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/c/cairo/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png c cairo
python3 parsarium.py run png c cairo controls/png/red-green.png
python3 parsarium.py replay png c cairo CORPUS_DIR runs/png-cairo-replay
python3 parsarium.py afl build png c cairo
python3 parsarium.py afl prepare png c cairo runs/png-cairo-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
