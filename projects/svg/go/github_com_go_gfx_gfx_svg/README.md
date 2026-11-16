# github.com/go-gfx/gfx/svg — SVG / Go

Pinned release: `v0.41.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/go/github-com-go-gfx-gfx-svg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg go github_com_go_gfx_gfx_svg
python3 parsarium.py run svg go github_com_go_gfx_gfx_svg controls/svg/red-green.svg
python3 parsarium.py replay svg go github_com_go_gfx_gfx_svg CORPUS_DIR runs/svg-github_com_go_gfx_gfx_svg-replay
python3 parsarium.py afl build svg go github_com_go_gfx_gfx_svg
python3 parsarium.py afl prepare svg go github_com_go_gfx_gfx_svg runs/svg-github_com_go_gfx_gfx_svg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
