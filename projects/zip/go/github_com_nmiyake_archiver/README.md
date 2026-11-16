# github.com/nmiyake/archiver — ZIP / Go

Pinned release: `v1.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/go/github-com-nmiyake-archiver/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip go github_com_nmiyake_archiver
python3 parsarium.py run zip go github_com_nmiyake_archiver controls/zip/hello.zip
python3 parsarium.py replay zip go github_com_nmiyake_archiver CORPUS_DIR runs/zip-github_com_nmiyake_archiver-replay
python3 parsarium.py afl build zip go github_com_nmiyake_archiver
python3 parsarium.py afl prepare zip go github_com_nmiyake_archiver runs/zip-github_com_nmiyake_archiver-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
