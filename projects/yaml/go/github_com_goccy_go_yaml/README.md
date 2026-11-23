# github.com/goccy/go-yaml — YAML / Go

Pinned release: `v1.19.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/go/github-com-goccy-go-yaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml go github_com_goccy_go_yaml
python3 parsarium.py run yaml go github_com_goccy_go_yaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml go github_com_goccy_go_yaml CORPUS_DIR runs/yaml-github_com_goccy_go_yaml-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build yaml go github_com_goccy_go_yaml
python3 parsarium.py afl prepare yaml go github_com_goccy_go_yaml runs/yaml-github_com_goccy_go_yaml-afl --fandango 100
python3 parsarium.py afl run runs/yaml-github_com_goccy_go_yaml-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
