# github.com/pgavlin/svg2 — SVG / Go

Pinned release: `v0.0.0-20210919231505-4ace7308edc1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/go/github-com-pgavlin-svg2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg go github_com_pgavlin_svg2
python3 parsarium.py run svg go github_com_pgavlin_svg2 controls/svg/red-green.svg
python3 parsarium.py replay svg go github_com_pgavlin_svg2 CORPUS_DIR runs/svg-github_com_pgavlin_svg2-replay
python3 parsarium.py afl build svg go github_com_pgavlin_svg2
python3 parsarium.py afl prepare svg go github_com_pgavlin_svg2 runs/svg-github_com_pgavlin_svg2-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
