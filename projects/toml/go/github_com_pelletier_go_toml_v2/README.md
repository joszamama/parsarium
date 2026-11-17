# github.com/pelletier/go-toml/v2 — TOML / Go

Pinned release: `v2.4.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/go/github-com-pelletier-go-toml-v2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml go github_com_pelletier_go_toml_v2
python3 parsarium.py run toml go github_com_pelletier_go_toml_v2 controls/toml/service-config.toml
python3 parsarium.py replay toml go github_com_pelletier_go_toml_v2 CORPUS_DIR runs/toml-github_com_pelletier_go_toml_v2-replay
python3 parsarium.py afl build toml go github_com_pelletier_go_toml_v2
python3 parsarium.py afl prepare toml go github_com_pelletier_go_toml_v2 runs/toml-github_com_pelletier_go_toml_v2-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
