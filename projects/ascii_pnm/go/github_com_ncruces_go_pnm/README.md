# github.com/ncruces/go-pnm — ASCII PNM / Go

Pinned release: `v1.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/go/github-com-ncruces-go-pnm/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm go github_com_ncruces_go_pnm
python3 parsarium.py run ascii_pnm go github_com_ncruces_go_pnm controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm go github_com_ncruces_go_pnm CORPUS_DIR runs/ascii_pnm-github_com_ncruces_go_pnm-replay
python3 parsarium.py afl build ascii_pnm go github_com_ncruces_go_pnm
python3 parsarium.py afl prepare ascii_pnm go github_com_ncruces_go_pnm runs/ascii_pnm-github_com_ncruces_go_pnm-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
