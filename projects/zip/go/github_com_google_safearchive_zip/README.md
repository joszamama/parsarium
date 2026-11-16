# github.com/google/safearchive/zip — ZIP / Go

Pinned release: `v0.0.0-20241025131057-f7ce9d7b6f9c`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/go/github-com-google-safearchive-zip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip go github_com_google_safearchive_zip
python3 parsarium.py run zip go github_com_google_safearchive_zip controls/zip/hello.zip
python3 parsarium.py replay zip go github_com_google_safearchive_zip CORPUS_DIR runs/zip-github_com_google_safearchive_zip-replay
python3 parsarium.py afl build zip go github_com_google_safearchive_zip
python3 parsarium.py afl prepare zip go github_com_google_safearchive_zip runs/zip-github_com_google_safearchive_zip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
