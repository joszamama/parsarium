# github.com/mholt/archives — ZIP / Go

Pinned release: `v0.1.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/go/github-com-mholt-archives/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip go github_com_mholt_archives
python3 parsarium.py run zip go github_com_mholt_archives controls/zip/hello.zip
python3 parsarium.py replay zip go github_com_mholt_archives CORPUS_DIR runs/zip-github_com_mholt_archives-replay
python3 parsarium.py afl build zip go github_com_mholt_archives
python3 parsarium.py afl prepare zip go github_com_mholt_archives runs/zip-github_com_mholt_archives-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
