# github.com/segmentio/encoding/json — JSON / Go

Pinned release: `v0.5.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/go/github-com-segmentio-encoding-json/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json go segmentio_encoding
python3 parsarium.py run json go segmentio_encoding controls/json/nested-object.json
python3 parsarium.py replay json go segmentio_encoding CORPUS_DIR runs/json-segmentio_encoding-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build json go segmentio_encoding
python3 parsarium.py afl prepare json go segmentio_encoding runs/json-segmentio_encoding-afl --fandango 100
python3 parsarium.py afl run runs/json-segmentio_encoding-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
