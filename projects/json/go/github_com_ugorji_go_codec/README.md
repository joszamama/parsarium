# github.com/ugorji/go/codec — JSON / Go

Pinned release: `v1.3.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/go/github-com-ugorji-go-codec/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json go github_com_ugorji_go_codec
python3 parsarium.py run json go github_com_ugorji_go_codec controls/json/nested-object.json
python3 parsarium.py replay json go github_com_ugorji_go_codec CORPUS_DIR runs/json-github_com_ugorji_go_codec-replay
python3 parsarium.py afl build json go github_com_ugorji_go_codec
python3 parsarium.py afl prepare json go github_com_ugorji_go_codec runs/json-github_com_ugorji_go_codec-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
