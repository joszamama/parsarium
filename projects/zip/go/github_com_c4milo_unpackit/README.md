# github.com/c4milo/unpackit — ZIP / Go

Pinned release: `v1.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/go/github-com-c4milo-unpackit/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip go github_com_c4milo_unpackit
python3 parsarium.py run zip go github_com_c4milo_unpackit controls/zip/hello.zip
python3 parsarium.py replay zip go github_com_c4milo_unpackit CORPUS_DIR runs/zip-github_com_c4milo_unpackit-replay
python3 parsarium.py afl build zip go github_com_c4milo_unpackit
python3 parsarium.py afl prepare zip go github_com_c4milo_unpackit runs/zip-github_com_c4milo_unpackit-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
