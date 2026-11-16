# github.com/sourcegraph/lazyzip — ZIP / Go

Pinned release: `v0.0.0-20180104141618-672a4b512c09`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/go/github-com-sourcegraph-lazyzip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip go github_com_sourcegraph_lazyzip
python3 parsarium.py run zip go github_com_sourcegraph_lazyzip controls/zip/hello.zip
python3 parsarium.py replay zip go github_com_sourcegraph_lazyzip CORPUS_DIR runs/zip-github_com_sourcegraph_lazyzip-replay
python3 parsarium.py afl build zip go github_com_sourcegraph_lazyzip
python3 parsarium.py afl prepare zip go github_com_sourcegraph_lazyzip runs/zip-github_com_sourcegraph_lazyzip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
