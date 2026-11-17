# laktak/hjson — JSON / PHP

Pinned release: `v2.3.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/php/laktak-hjson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json php laktak_hjson
python3 parsarium.py run json php laktak_hjson controls/json/nested-object.json
python3 parsarium.py replay json php laktak_hjson CORPUS_DIR runs/json-laktak_hjson-replay
python3 parsarium.py afl build json php laktak_hjson
python3 parsarium.py afl prepare json php laktak_hjson runs/json-laktak_hjson-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
