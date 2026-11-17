# github.com/json-iterator/go — JSON / Go

Pinned release: `v1.1.12`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Cell ranking, lead log, and parser family](../../../../data/go/json/ranking.md)

## Run from the repository root

```sh
python3 parsarium.py build json go github_com_json_iterator_go
python3 parsarium.py run json go github_com_json_iterator_go controls/json/nested-object.json
python3 parsarium.py replay json go github_com_json_iterator_go CORPUS_DIR runs/json-github_com_json_iterator_go-replay
python3 parsarium.py afl build json go github_com_json_iterator_go
python3 parsarium.py afl prepare json go github_com_json_iterator_go runs/json-github_com_json_iterator_go-afl
python3 scripts/verify_go_json_feedback.py
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign. `verify_go_json_feedback.py` repeats the control probe and compares it with the second valid control, `controls/json/nested-array.json`.
