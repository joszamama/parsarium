# github.com/bytedance/sonic — JSON / Go

Pinned release: `v1.15.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/go/github-com-bytedance-sonic/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json go github_com_bytedance_sonic
python3 parsarium.py run json go github_com_bytedance_sonic controls/json/nested-object.json
python3 parsarium.py replay json go github_com_bytedance_sonic CORPUS_DIR runs/json-github_com_bytedance_sonic-replay
python3 parsarium.py afl build json go github_com_bytedance_sonic
python3 parsarium.py afl prepare json go github_com_bytedance_sonic runs/json-github_com_bytedance_sonic-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
