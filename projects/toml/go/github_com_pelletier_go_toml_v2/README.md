# github.com/pelletier/go-toml/v2 — TOML / Go

Pinned release: `v2.4.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/go/github-com-pelletier-go-toml-v2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml go github_com_pelletier_go_toml_v2
python3 parsarium.py run toml go github_com_pelletier_go_toml_v2 controls/toml/service-config.toml
python3 parsarium.py replay toml go github_com_pelletier_go_toml_v2 CORPUS_DIR runs/toml-github_com_pelletier_go_toml_v2-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build toml go github_com_pelletier_go_toml_v2
python3 parsarium.py afl prepare toml go github_com_pelletier_go_toml_v2 runs/toml-github_com_pelletier_go_toml_v2-afl --fandango 100
python3 parsarium.py afl run runs/toml-github_com_pelletier_go_toml_v2-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
