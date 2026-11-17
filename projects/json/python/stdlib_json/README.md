# CPython `json` — JSON / Python standard library

Pinned runtime: CPython `3.14.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Official API, control, and parser scope](../../../../catalog/json/python/stdlib_json/README.md)

Run from the repository root:

```sh
python3 parsarium.py build json python stdlib_json
python3 parsarium.py run json python stdlib_json controls/json/structure.json
python3 parsarium.py replay json python stdlib_json CORPUS_DIR runs/json-stdlib-replay
python3 parsarium.py afl build json python stdlib_json
python3 parsarium.py afl prepare json python stdlib_json runs/json-stdlib-afl
```

`CORPUS_DIR` holds JSON files for one-file replay. AFL++ preparation writes a run plan and seeds; it does not start a campaign.
