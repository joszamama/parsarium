# halaxa/json-machine — JSON / PHP

Pinned release: `1.2.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, controls, and parser family](../../../../catalog/json/php/halaxa-json-machine/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json php halaxa_json_machine
python3 parsarium.py run json php halaxa_json_machine controls/json/nested-object.json
python3 parsarium.py replay json php halaxa_json_machine CORPUS_DIR runs/json-php-machine-replay
python3 parsarium.py afl build json php halaxa_json_machine
python3 parsarium.py afl prepare json php halaxa_json_machine runs/json-php-machine-afl
python3 parsarium.py afl run runs/json-php-machine-afl --check
```

AFL++ preparation creates a seeded run. The check command verifies the launch configuration without starting a campaign.
