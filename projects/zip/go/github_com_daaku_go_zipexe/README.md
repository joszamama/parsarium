# github.com/daaku/go.zipexe — ZIP / Go

Pinned release: `v1.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/go/github-com-daaku-go-zipexe/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip go github_com_daaku_go_zipexe
python3 parsarium.py run zip go github_com_daaku_go_zipexe controls/zip/hello.zip
python3 parsarium.py replay zip go github_com_daaku_go_zipexe CORPUS_DIR runs/zip-github_com_daaku_go_zipexe-replay
python3 parsarium.py afl build zip go github_com_daaku_go_zipexe
python3 parsarium.py afl prepare zip go github_com_daaku_go_zipexe runs/zip-github_com_daaku_go_zipexe-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
