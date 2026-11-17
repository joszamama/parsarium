# parsson — JSON / Java

Pinned release: `1.1.9`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/java/parsson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json java parsson
python3 parsarium.py run json java parsson controls/json/nested-object.json
python3 parsarium.py replay json java parsson CORPUS_DIR runs/json-parsson-replay
python3 parsarium.py afl build json java parsson
python3 parsarium.py afl prepare json java parsson runs/json-parsson-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
