# github.com/vibrantgio/svg/parser — SVG / Go

Pinned release: `v0.1.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/go/github-com-vibrantgio-svg-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg go github_com_vibrantgio_svg_parser
python3 parsarium.py run svg go github_com_vibrantgio_svg_parser controls/svg/red-green.svg
python3 parsarium.py replay svg go github_com_vibrantgio_svg_parser CORPUS_DIR runs/svg-github_com_vibrantgio_svg_parser-replay
python3 parsarium.py afl build svg go github_com_vibrantgio_svg_parser
python3 parsarium.py afl prepare svg go github_com_vibrantgio_svg_parser runs/svg-github_com_vibrantgio_svg_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
