# github.com/go-rotini/yaml — YAML / Go

Pinned release: `v1.2.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/go/github-com-go-rotini-yaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml go github_com_go_rotini_yaml
python3 parsarium.py run yaml go github_com_go_rotini_yaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml go github_com_go_rotini_yaml CORPUS_DIR runs/yaml-github_com_go_rotini_yaml-replay
python3 parsarium.py afl build yaml go github_com_go_rotini_yaml
python3 parsarium.py afl prepare yaml go github_com_go_rotini_yaml runs/yaml-github_com_go_rotini_yaml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
