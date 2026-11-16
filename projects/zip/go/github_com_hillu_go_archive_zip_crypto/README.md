# github.com/hillu/go-archive-zip-crypto — ZIP / Go

Pinned release: `v0.0.0-20200712202847-bd5cf365dd44`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/go/github-com-hillu-go-archive-zip-crypto/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip go github_com_hillu_go_archive_zip_crypto
python3 parsarium.py run zip go github_com_hillu_go_archive_zip_crypto controls/zip/hello.zip
python3 parsarium.py replay zip go github_com_hillu_go_archive_zip_crypto CORPUS_DIR runs/zip-github_com_hillu_go_archive_zip_crypto-replay
python3 parsarium.py afl build zip go github_com_hillu_go_archive_zip_crypto
python3 parsarium.py afl prepare zip go github_com_hillu_go_archive_zip_crypto runs/zip-github_com_hillu_go_archive_zip_crypto-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
