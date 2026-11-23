# aws-smithy-json — JSON / Rust

Pinned release: `0.65.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/rust/aws-smithy-json/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json rust aws_smithy_json
python3 parsarium.py run json rust aws_smithy_json controls/json/nested-object.json
python3 parsarium.py replay json rust aws_smithy_json CORPUS_DIR runs/json-aws_smithy_json-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build json rust aws_smithy_json
python3 parsarium.py afl prepare json rust aws_smithy_json runs/json-aws_smithy_json-afl --fandango 100
python3 parsarium.py afl run runs/json-aws_smithy_json-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
