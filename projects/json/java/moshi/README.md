# moshi — JSON / Java

Pinned release: `1.15.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/java/moshi/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json java moshi
python3 parsarium.py run json java moshi controls/json/nested-object.json
python3 parsarium.py replay json java moshi CORPUS_DIR runs/json-moshi-replay
python3 parsarium.py afl build json java moshi
python3 parsarium.py afl prepare json java moshi runs/json-moshi-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
