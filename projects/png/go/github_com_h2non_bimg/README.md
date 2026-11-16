# github.com/h2non/bimg — PNG / Go

Pinned release: `v1.1.9`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/go/github-com-h2non-bimg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png go github_com_h2non_bimg
python3 parsarium.py run png go github_com_h2non_bimg controls/png/red-green.png
python3 parsarium.py replay png go github_com_h2non_bimg CORPUS_DIR runs/png-github_com_h2non_bimg-replay
python3 parsarium.py afl build png go github_com_h2non_bimg
python3 parsarium.py afl prepare png go github_com_h2non_bimg runs/png-github_com_h2non_bimg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
