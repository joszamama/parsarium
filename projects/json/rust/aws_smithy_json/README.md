# aws-smithy-json — JSON / Rust

Pinned release: `0.65.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/rust/aws-smithy-json/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json rust aws_smithy_json
python3 parsarium.py run json rust aws_smithy_json controls/json/nested-object.json
python3 parsarium.py replay json rust aws_smithy_json CORPUS_DIR runs/json-aws_smithy_json-replay
python3 parsarium.py afl build json rust aws_smithy_json
python3 parsarium.py afl prepare json rust aws_smithy_json runs/json-aws_smithy_json-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
