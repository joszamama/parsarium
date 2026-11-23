# github.com/buger/jsonparser — JSON / Go

Pinned release: `v1.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/go/github-com-buger-jsonparser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json go github_com_buger_jsonparser
python3 parsarium.py run json go github_com_buger_jsonparser controls/json/nested-object.json
python3 parsarium.py replay json go github_com_buger_jsonparser CORPUS_DIR runs/json-github_com_buger_jsonparser-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build json go github_com_buger_jsonparser
python3 parsarium.py afl prepare json go github_com_buger_jsonparser runs/json-github_com_buger_jsonparser-afl --fandango 100
python3 parsarium.py afl run runs/json-github_com_buger_jsonparser-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
