# github.com/yongjohnlee80/golib/parse/yaml — YAML / Go

Pinned release: `v0.8.62`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/go/github-com-yongjohnlee80-golib-parse-yaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml go github_com_yongjohnlee80_golib_parse_yaml
python3 parsarium.py run yaml go github_com_yongjohnlee80_golib_parse_yaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml go github_com_yongjohnlee80_golib_parse_yaml CORPUS_DIR runs/yaml-github_com_yongjohnlee80_golib_parse_yaml-replay
python3 parsarium.py afl build yaml go github_com_yongjohnlee80_golib_parse_yaml
python3 parsarium.py afl prepare yaml go github_com_yongjohnlee80_golib_parse_yaml runs/yaml-github_com_yongjohnlee80_golib_parse_yaml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
