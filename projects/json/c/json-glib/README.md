# json-glib — JSON / C

Pinned release: `1.10.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/c/json-glib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json c json-glib
python3 parsarium.py run json c json-glib controls/json/nested-object.json
python3 parsarium.py replay json c json-glib CORPUS_DIR runs/json-json-glib-replay
python3 parsarium.py afl build json c json-glib
python3 parsarium.py afl prepare json c json-glib runs/json-json-glib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
