# github.com/fogleman/gg — PNG / Go

Pinned release: `v1.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/go/github-com-fogleman-gg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png go github_com_fogleman_gg
python3 parsarium.py run png go github_com_fogleman_gg controls/png/red-green.png
python3 parsarium.py replay png go github_com_fogleman_gg CORPUS_DIR runs/png-github_com_fogleman_gg-replay
python3 parsarium.py afl build png go github_com_fogleman_gg
python3 parsarium.py afl prepare png go github_com_fogleman_gg runs/png-github_com_fogleman_gg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
