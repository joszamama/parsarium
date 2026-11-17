# github.com/goccy/go-json — JSON / Go

Pinned release: `v0.12.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/go/github-com-goccy-go-json/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json go github_com_goccy_go_json
python3 parsarium.py run json go github_com_goccy_go_json controls/json/nested-object.json
python3 parsarium.py replay json go github_com_goccy_go_json CORPUS_DIR runs/json-github_com_goccy_go_json-replay
python3 parsarium.py afl build json go github_com_goccy_go_json
python3 parsarium.py afl prepare json go github_com_goccy_go_json runs/json-github_com_goccy_go_json-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
