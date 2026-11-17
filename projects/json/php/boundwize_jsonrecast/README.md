# boundwize/jsonrecast — JSON / PHP

Pinned release: `1.0.37`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/php/boundwize-jsonrecast/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json php boundwize_jsonrecast
python3 parsarium.py run json php boundwize_jsonrecast controls/json/nested-object.json
python3 parsarium.py replay json php boundwize_jsonrecast CORPUS_DIR runs/json-boundwize_jsonrecast-replay
python3 parsarium.py afl build json php boundwize_jsonrecast
python3 parsarium.py afl prepare json php boundwize_jsonrecast runs/json-boundwize_jsonrecast-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
