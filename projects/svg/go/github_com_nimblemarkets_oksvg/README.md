# github.com/NimbleMarkets/oksvg — SVG / Go

Pinned release: `v0.1.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/go/github-com-nimblemarkets-oksvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg go github_com_nimblemarkets_oksvg
python3 parsarium.py run svg go github_com_nimblemarkets_oksvg controls/svg/red-green.svg
python3 parsarium.py replay svg go github_com_nimblemarkets_oksvg CORPUS_DIR runs/svg-github_com_nimblemarkets_oksvg-replay
python3 parsarium.py afl build svg go github_com_nimblemarkets_oksvg
python3 parsarium.py afl prepare svg go github_com_nimblemarkets_oksvg runs/svg-github_com_nimblemarkets_oksvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
