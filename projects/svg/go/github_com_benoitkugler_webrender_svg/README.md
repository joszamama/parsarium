# github.com/benoitkugler/webrender/svg — SVG / Go

Pinned release: `v0.0.15`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/go/github-com-benoitkugler-webrender-svg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg go github_com_benoitkugler_webrender_svg
python3 parsarium.py run svg go github_com_benoitkugler_webrender_svg controls/svg/red-green.svg
python3 parsarium.py replay svg go github_com_benoitkugler_webrender_svg CORPUS_DIR runs/svg-github_com_benoitkugler_webrender_svg-replay
python3 parsarium.py afl build svg go github_com_benoitkugler_webrender_svg
python3 parsarium.py afl prepare svg go github_com_benoitkugler_webrender_svg runs/svg-github_com_benoitkugler_webrender_svg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
