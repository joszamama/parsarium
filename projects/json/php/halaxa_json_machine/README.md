# halaxa/json-machine — JSON / PHP

Pinned release: `1.2.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/php/halaxa-json-machine/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json php halaxa_json_machine
python3 parsarium.py run json php halaxa_json_machine controls/json/nested-object.json
python3 parsarium.py replay json php halaxa_json_machine CORPUS_DIR runs/json-halaxa_json_machine-replay
python3 parsarium.py afl build json php halaxa_json_machine
python3 parsarium.py afl prepare json php halaxa_json_machine runs/json-halaxa_json_machine-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
