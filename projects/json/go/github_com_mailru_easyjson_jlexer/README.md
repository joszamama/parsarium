# github.com/mailru/easyjson/jlexer — JSON / Go

Pinned release: `v0.9.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/go/github-com-mailru-easyjson-jlexer/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json go github_com_mailru_easyjson_jlexer
python3 parsarium.py run json go github_com_mailru_easyjson_jlexer controls/json/nested-object.json
python3 parsarium.py replay json go github_com_mailru_easyjson_jlexer CORPUS_DIR runs/json-github_com_mailru_easyjson_jlexer-replay
python3 parsarium.py afl build json go github_com_mailru_easyjson_jlexer
python3 parsarium.py afl prepare json go github_com_mailru_easyjson_jlexer runs/json-github_com_mailru_easyjson_jlexer-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
