# eftec/services_json — JSON / PHP

Pinned release: `2.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/php/eftec-services-json/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json php eftec_services_json
python3 parsarium.py run json php eftec_services_json controls/json/nested-object.json
python3 parsarium.py replay json php eftec_services_json CORPUS_DIR runs/json-eftec_services_json-replay
python3 parsarium.py afl build json php eftec_services_json
python3 parsarium.py afl prepare json php eftec_services_json runs/json-eftec_services_json-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
