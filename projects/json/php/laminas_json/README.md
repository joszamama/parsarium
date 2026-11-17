# laminas/laminas-json — JSON / PHP

Pinned release: `3.8.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, controls, and parser family](../../../../catalog/json/php/laminas-laminas-json/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json php laminas_json
python3 parsarium.py run json php laminas_json controls/json/nested-object.json
python3 parsarium.py replay json php laminas_json CORPUS_DIR runs/json-laminas-json-replay
python3 parsarium.py afl build json php laminas_json
python3 parsarium.py afl prepare json php laminas_json runs/json-laminas-json-afl
python3 parsarium.py afl run runs/json-laminas-json-afl --check
```

The adapter enables Laminas' own PHP decoder explicitly. Without that flag, `Json::decode()` calls PHP ext/json. AFL++ preparation creates a seeded run; the check command verifies the launch configuration without starting a campaign.
