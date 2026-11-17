# github.com/valyala/fastjson — JSON / Go

Pinned release: `v1.6.10`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/go/github-com-valyala-fastjson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json go github_com_valyala_fastjson
python3 parsarium.py run json go github_com_valyala_fastjson controls/json/nested-object.json
python3 parsarium.py replay json go github_com_valyala_fastjson CORPUS_DIR runs/json-github_com_valyala_fastjson-replay
python3 parsarium.py afl build json go github_com_valyala_fastjson
python3 parsarium.py afl prepare json go github_com_valyala_fastjson runs/json-github_com_valyala_fastjson-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
