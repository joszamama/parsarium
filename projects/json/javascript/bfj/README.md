# bfj — JSON / JavaScript

Pinned release: `9.1.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/javascript/bfj/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json javascript bfj
python3 parsarium.py run json javascript bfj controls/json/nested-object.json
python3 parsarium.py replay json javascript bfj CORPUS_DIR runs/json-bfj-replay
python3 parsarium.py afl build json javascript bfj
python3 parsarium.py afl prepare json javascript bfj runs/json-bfj-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
