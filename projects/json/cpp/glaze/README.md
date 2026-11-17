# Glaze — JSON / C++

Pinned release: `9.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/cpp/glaze/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json cpp glaze
python3 parsarium.py run json cpp glaze controls/json/nested-object.json
python3 parsarium.py replay json cpp glaze CORPUS_DIR runs/json-glaze-replay
python3 parsarium.py afl build json cpp glaze
python3 parsarium.py afl prepare json cpp glaze runs/json-glaze-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
