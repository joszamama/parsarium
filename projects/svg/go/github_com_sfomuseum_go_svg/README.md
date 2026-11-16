# github.com/sfomuseum/go-svg — SVG / Go

Pinned release: `v0.0.0-20231208192434-a3c9facf873c`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/go/github-com-sfomuseum-go-svg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg go github_com_sfomuseum_go_svg
python3 parsarium.py run svg go github_com_sfomuseum_go_svg controls/svg/red-green.svg
python3 parsarium.py replay svg go github_com_sfomuseum_go_svg CORPUS_DIR runs/svg-github_com_sfomuseum_go_svg-replay
python3 parsarium.py afl build svg go github_com_sfomuseum_go_svg
python3 parsarium.py afl prepare svg go github_com_sfomuseum_go_svg runs/svg-github_com_sfomuseum_go_svg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
