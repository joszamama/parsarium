# github.com/oyamo/pngx — PNG / Go

Pinned release: `v0.0.0-20230307064515-ec4b3bce8a92`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/go/github-com-oyamo-pngx/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png go github_com_oyamo_pngx
python3 parsarium.py run png go github_com_oyamo_pngx controls/png/red-green.png
python3 parsarium.py replay png go github_com_oyamo_pngx CORPUS_DIR runs/png-github_com_oyamo_pngx-replay
python3 parsarium.py afl build png go github_com_oyamo_pngx
python3 parsarium.py afl prepare png go github_com_oyamo_pngx runs/png-github_com_oyamo_pngx-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
