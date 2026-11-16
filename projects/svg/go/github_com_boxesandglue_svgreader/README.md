# github.com/boxesandglue/svgreader — SVG / Go

Pinned release: `v0.0.9`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/go/github-com-boxesandglue-svgreader/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg go github_com_boxesandglue_svgreader
python3 parsarium.py run svg go github_com_boxesandglue_svgreader controls/svg/red-green.svg
python3 parsarium.py replay svg go github_com_boxesandglue_svgreader CORPUS_DIR runs/svg-github_com_boxesandglue_svgreader-replay
python3 parsarium.py afl build svg go github_com_boxesandglue_svgreader
python3 parsarium.py afl prepare svg go github_com_boxesandglue_svgreader runs/svg-github_com_boxesandglue_svgreader-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
