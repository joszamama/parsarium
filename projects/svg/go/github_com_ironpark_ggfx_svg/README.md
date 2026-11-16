# github.com/ironpark/ggfx/svg — SVG / Go

Pinned release: `v0.0.0-20261111143539-00f0f2c03daa`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/go/github-com-ironpark-ggfx-svg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg go github_com_ironpark_ggfx_svg
python3 parsarium.py run svg go github_com_ironpark_ggfx_svg controls/svg/red-green.svg
python3 parsarium.py replay svg go github_com_ironpark_ggfx_svg CORPUS_DIR runs/svg-github_com_ironpark_ggfx_svg-replay
python3 parsarium.py afl build svg go github_com_ironpark_ggfx_svg
python3 parsarium.py afl prepare svg go github_com_ironpark_ggfx_svg runs/svg-github_com_ironpark_ggfx_svg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
