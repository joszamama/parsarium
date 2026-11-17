# fastjson — JSON / Java

Pinned release: `1.2.83`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/java/fastjson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json java fastjson1
python3 parsarium.py run json java fastjson1 controls/json/nested-object.json
python3 parsarium.py replay json java fastjson1 CORPUS_DIR runs/json-fastjson1-replay
python3 parsarium.py afl build json java fastjson1
python3 parsarium.py afl prepare json java fastjson1 runs/json-fastjson1-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
