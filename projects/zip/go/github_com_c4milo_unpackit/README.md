# github.com/c4milo/unpackit — ZIP / Go

Pinned release: `v1.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/go/github-com-c4milo-unpackit/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip go github_com_c4milo_unpackit
python3 parsarium.py run zip go github_com_c4milo_unpackit controls/zip/hello.zip
python3 parsarium.py replay zip go github_com_c4milo_unpackit CORPUS_DIR runs/zip-github_com_c4milo_unpackit-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build zip go github_com_c4milo_unpackit
python3 parsarium.py afl prepare zip go github_com_c4milo_unpackit runs/zip-github_com_c4milo_unpackit-afl --fandango 100
python3 parsarium.py afl run runs/zip-github_com_c4milo_unpackit-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
