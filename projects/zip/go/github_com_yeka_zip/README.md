# github.com/yeka/zip — ZIP / Go

Pinned release: `v0.0.0-20231116150916-03d6312748a9`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/go/github-com-yeka-zip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip go github_com_yeka_zip
python3 parsarium.py run zip go github_com_yeka_zip controls/zip/hello.zip
python3 parsarium.py replay zip go github_com_yeka_zip CORPUS_DIR runs/zip-github_com_yeka_zip-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build zip go github_com_yeka_zip
python3 parsarium.py afl prepare zip go github_com_yeka_zip runs/zip-github_com_yeka_zip-afl --fandango 100
python3 parsarium.py afl run runs/zip-github_com_yeka_zip-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
