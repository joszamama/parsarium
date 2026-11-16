# github.com/krolaw/zipstream — ZIP / Go

Pinned release: `v0.0.0-20241109034754-4a67be70fe31`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/go/github-com-krolaw-zipstream/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip go github_com_krolaw_zipstream
python3 parsarium.py run zip go github_com_krolaw_zipstream controls/zip/hello.zip
python3 parsarium.py replay zip go github_com_krolaw_zipstream CORPUS_DIR runs/zip-github_com_krolaw_zipstream-replay
python3 parsarium.py afl build zip go github_com_krolaw_zipstream
python3 parsarium.py afl prepare zip go github_com_krolaw_zipstream runs/zip-github_com_krolaw_zipstream-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
