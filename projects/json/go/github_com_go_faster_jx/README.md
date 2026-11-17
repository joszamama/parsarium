# github.com/go-faster/jx — JSON / Go

Pinned release: `v1.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/go/github-com-go-faster-jx/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json go github_com_go_faster_jx
python3 parsarium.py run json go github_com_go_faster_jx controls/json/nested-object.json
python3 parsarium.py replay json go github_com_go_faster_jx CORPUS_DIR runs/json-github_com_go_faster_jx-replay
python3 parsarium.py afl build json go github_com_go_faster_jx
python3 parsarium.py afl prepare json go github_com_go_faster_jx runs/json-github_com_go_faster_jx-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
