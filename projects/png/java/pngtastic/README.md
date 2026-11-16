# pngtastic — PNG / Java

Pinned release: `1.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/java/pngtastic/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png java pngtastic
python3 parsarium.py run png java pngtastic controls/png/red-green.png
python3 parsarium.py replay png java pngtastic CORPUS_DIR runs/png-pngtastic-replay
python3 parsarium.py afl build png java pngtastic
python3 parsarium.py afl prepare png java pngtastic runs/png-pngtastic-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
