# github.com/JoshVarga/svgparser — SVG / Go

Pinned release: `v0.0.0-20200804023048-5eaba627a7d1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/go/github-com-joshvarga-svgparser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg go github_com_joshvarga_svgparser
python3 parsarium.py run svg go github_com_joshvarga_svgparser controls/svg/red-green.svg
python3 parsarium.py replay svg go github_com_joshvarga_svgparser CORPUS_DIR runs/svg-github_com_joshvarga_svgparser-replay
python3 parsarium.py afl build svg go github_com_joshvarga_svgparser
python3 parsarium.py afl prepare svg go github_com_joshvarga_svgparser runs/svg-github_com_joshvarga_svgparser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
