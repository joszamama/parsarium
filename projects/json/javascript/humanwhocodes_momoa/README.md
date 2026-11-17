# @humanwhocodes/momoa — JSON / JavaScript

Pinned release: `3.3.13`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/javascript/humanwhocodes-momoa/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json javascript humanwhocodes_momoa
python3 parsarium.py run json javascript humanwhocodes_momoa controls/json/nested-object.json
python3 parsarium.py replay json javascript humanwhocodes_momoa CORPUS_DIR runs/json-humanwhocodes_momoa-replay
python3 parsarium.py afl build json javascript humanwhocodes_momoa
python3 parsarium.py afl prepare json javascript humanwhocodes_momoa runs/json-humanwhocodes_momoa-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
