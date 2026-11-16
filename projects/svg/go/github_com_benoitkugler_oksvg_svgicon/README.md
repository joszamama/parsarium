# github.com/benoitkugler/oksvg/svgicon — SVG / Go

Pinned release: `v0.0.0-20230818175515-13805796eb24`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/go/github-com-benoitkugler-oksvg-svgicon/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg go github_com_benoitkugler_oksvg_svgicon
python3 parsarium.py run svg go github_com_benoitkugler_oksvg_svgicon controls/svg/red-green.svg
python3 parsarium.py replay svg go github_com_benoitkugler_oksvg_svgicon CORPUS_DIR runs/svg-github_com_benoitkugler_oksvg_svgicon-replay
python3 parsarium.py afl build svg go github_com_benoitkugler_oksvg_svgicon
python3 parsarium.py afl prepare svg go github_com_benoitkugler_oksvg_svgicon runs/svg-github_com_benoitkugler_oksvg_svgicon-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
