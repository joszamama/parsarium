# github.com/tidwall/gjson — JSON / Go

Pinned release: `v1.20.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/go/github-com-tidwall-gjson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json go github_com_tidwall_gjson
python3 parsarium.py run json go github_com_tidwall_gjson controls/json/nested-object.json
python3 parsarium.py replay json go github_com_tidwall_gjson CORPUS_DIR runs/json-github_com_tidwall_gjson-replay
python3 parsarium.py afl build json go github_com_tidwall_gjson
python3 parsarium.py afl prepare json go github_com_tidwall_gjson runs/json-github_com_tidwall_gjson-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
