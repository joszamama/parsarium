# github.com/unknwon/cae/zip — ZIP / Go

Pinned release: `v1.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/go/github-com-unknwon-cae-zip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip go github_com_unknwon_cae_zip
python3 parsarium.py run zip go github_com_unknwon_cae_zip controls/zip/hello.zip
python3 parsarium.py replay zip go github_com_unknwon_cae_zip CORPUS_DIR runs/zip-github_com_unknwon_cae_zip-replay
python3 parsarium.py afl build zip go github_com_unknwon_cae_zip
python3 parsarium.py afl prepare zip go github_com_unknwon_cae_zip runs/zip-github_com_unknwon_cae_zip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
