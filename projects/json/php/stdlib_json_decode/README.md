# php-json-decode — JSON / PHP

Pinned release: `8.5.12`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/php/json/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build json php stdlib_json_decode
python3 parsarium.py run json php stdlib_json_decode controls/json/nested-object.json
python3 parsarium.py replay json php stdlib_json_decode CORPUS_DIR runs/json-stdlib_json_decode-replay
python3 parsarium.py afl build json php stdlib_json_decode
python3 parsarium.py afl prepare json php stdlib_json_decode runs/json-stdlib_json_decode-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
