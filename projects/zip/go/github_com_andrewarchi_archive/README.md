# github.com/andrewarchi/archive — ZIP / Go

Pinned release: `v0.0.0-20210213193640-3a6449eed2ec`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/go/github-com-andrewarchi-archive/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip go github_com_andrewarchi_archive
python3 parsarium.py run zip go github_com_andrewarchi_archive controls/zip/hello.zip
python3 parsarium.py replay zip go github_com_andrewarchi_archive CORPUS_DIR runs/zip-github_com_andrewarchi_archive-replay
python3 parsarium.py afl build zip go github_com_andrewarchi_archive
python3 parsarium.py afl prepare zip go github_com_andrewarchi_archive runs/zip-github_com_andrewarchi_archive-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
