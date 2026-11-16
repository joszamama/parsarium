# github.com/STARRY-S/zip — ZIP / Go

Pinned release: `v0.2.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/go/github-com-starry-s-zip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip go github_com_starry_s_zip
python3 parsarium.py run zip go github_com_starry_s_zip controls/zip/hello.zip
python3 parsarium.py replay zip go github_com_starry_s_zip CORPUS_DIR runs/zip-github_com_starry_s_zip-replay
python3 parsarium.py afl build zip go github_com_starry_s_zip
python3 parsarium.py afl prepare zip go github_com_starry_s_zip runs/zip-github_com_starry_s_zip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
