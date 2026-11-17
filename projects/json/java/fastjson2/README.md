# fastjson2 — JSON / Java

Pinned release: `2.0.66`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/java/fastjson2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json java fastjson2
python3 parsarium.py run json java fastjson2 controls/json/nested-object.json
python3 parsarium.py replay json java fastjson2 CORPUS_DIR runs/json-fastjson2-replay
python3 parsarium.py afl build json java fastjson2
python3 parsarium.py afl prepare json java fastjson2 runs/json-fastjson2-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
