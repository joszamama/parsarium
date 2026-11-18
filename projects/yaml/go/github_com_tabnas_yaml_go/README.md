# github.com/tabnas/yaml/go — YAML / Go

Pinned release: `v0.5.32`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/go/github-com-tabnas-yaml-go/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml go github_com_tabnas_yaml_go
python3 parsarium.py run yaml go github_com_tabnas_yaml_go controls/yaml/catalog.yaml
python3 parsarium.py replay yaml go github_com_tabnas_yaml_go CORPUS_DIR runs/yaml-github_com_tabnas_yaml_go-replay
python3 parsarium.py afl build yaml go github_com_tabnas_yaml_go
python3 parsarium.py afl prepare yaml go github_com_tabnas_yaml_go runs/yaml-github_com_tabnas_yaml_go-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
