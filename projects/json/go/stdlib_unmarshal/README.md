# encoding/json.Unmarshal([]byte, any) — JSON / Go

Pinned release: `1.27.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/go/json/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build json go stdlib_unmarshal
python3 parsarium.py run json go stdlib_unmarshal controls/json/nested-object.json
python3 parsarium.py replay json go stdlib_unmarshal CORPUS_DIR runs/json-stdlib_unmarshal-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build json go stdlib_unmarshal
python3 parsarium.py afl prepare json go stdlib_unmarshal runs/json-stdlib_unmarshal-afl --fandango 100
python3 parsarium.py afl run runs/json-stdlib_unmarshal-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
