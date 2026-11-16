# github.com/codeclysm/extract/v4 — ZIP / Go

Pinned release: `v4.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/go/github-com-codeclysm-extract-v4/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip go github_com_codeclysm_extract_v4
python3 parsarium.py run zip go github_com_codeclysm_extract_v4 controls/zip/hello.zip
python3 parsarium.py replay zip go github_com_codeclysm_extract_v4 CORPUS_DIR runs/zip-github_com_codeclysm_extract_v4-replay
python3 parsarium.py afl build zip go github_com_codeclysm_extract_v4
python3 parsarium.py afl prepare zip go github_com_codeclysm_extract_v4 runs/zip-github_com_codeclysm_extract_v4-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
