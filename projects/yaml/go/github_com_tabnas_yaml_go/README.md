# github.com/tabnas/yaml/go — YAML / Go

Pinned release: `v0.5.32`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/go/github-com-tabnas-yaml-go/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml go github_com_tabnas_yaml_go
python3 parsarium.py run yaml go github_com_tabnas_yaml_go controls/yaml/catalog.yaml
python3 parsarium.py replay yaml go github_com_tabnas_yaml_go CORPUS_DIR runs/yaml-github_com_tabnas_yaml_go-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build yaml go github_com_tabnas_yaml_go
python3 parsarium.py afl prepare yaml go github_com_tabnas_yaml_go runs/yaml-github_com_tabnas_yaml_go-afl --fandango 100
python3 parsarium.py afl run runs/yaml-github_com_tabnas_yaml_go-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
