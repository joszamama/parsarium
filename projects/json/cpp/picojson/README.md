# PicoJSON — JSON / C++

Pinned release: `1.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/cpp/picojson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json cpp picojson
python3 parsarium.py run json cpp picojson controls/json/nested-object.json
python3 parsarium.py replay json cpp picojson CORPUS_DIR runs/json-picojson-replay
python3 parsarium.py afl build json cpp picojson
python3 parsarium.py afl prepare json cpp picojson runs/json-picojson-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
