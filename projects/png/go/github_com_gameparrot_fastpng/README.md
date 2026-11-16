# github.com/gameparrot/fastpng — PNG / Go

Pinned release: `v0.0.0-20250305185850-d72e123a2123`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/go/github-com-gameparrot-fastpng/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png go github_com_gameparrot_fastpng
python3 parsarium.py run png go github_com_gameparrot_fastpng controls/png/red-green.png
python3 parsarium.py replay png go github_com_gameparrot_fastpng CORPUS_DIR runs/png-github_com_gameparrot_fastpng-replay
python3 parsarium.py afl build png go github_com_gameparrot_fastpng
python3 parsarium.py afl prepare png go github_com_gameparrot_fastpng runs/png-github_com_gameparrot_fastpng-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
