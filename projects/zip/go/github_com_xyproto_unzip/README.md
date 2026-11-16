# github.com/xyproto/unzip — ZIP / Go

Pinned release: `v1.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/go/github-com-xyproto-unzip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip go github_com_xyproto_unzip
python3 parsarium.py run zip go github_com_xyproto_unzip controls/zip/hello.zip
python3 parsarium.py replay zip go github_com_xyproto_unzip CORPUS_DIR runs/zip-github_com_xyproto_unzip-replay
python3 parsarium.py afl build zip go github_com_xyproto_unzip
python3 parsarium.py afl prepare zip go github_com_xyproto_unzip runs/zip-github_com_xyproto_unzip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
