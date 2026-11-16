# nette/utils — PNG / PHP

Pinned release: `v4.1.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/php/nette-utils/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png php nette_utils
python3 parsarium.py run png php nette_utils controls/png/red-green.png
python3 parsarium.py replay png php nette_utils CORPUS_DIR runs/png-nette_utils-replay
python3 parsarium.py afl build png php nette_utils
python3 parsarium.py afl prepare png php nette_utils runs/png-nette_utils-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
