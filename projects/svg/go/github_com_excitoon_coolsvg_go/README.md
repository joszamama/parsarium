# github.com/excitoon/coolsvg-go — SVG / Go

Pinned release: `v0.0.0-20260812001811-a8ecd1868275`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/go/github-com-excitoon-coolsvg-go/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg go github_com_excitoon_coolsvg_go
python3 parsarium.py run svg go github_com_excitoon_coolsvg_go controls/svg/red-green.svg
python3 parsarium.py replay svg go github_com_excitoon_coolsvg_go CORPUS_DIR runs/svg-github_com_excitoon_coolsvg_go-replay
python3 parsarium.py afl build svg go github_com_excitoon_coolsvg_go
python3 parsarium.py afl prepare svg go github_com_excitoon_coolsvg_go runs/svg-github_com_excitoon_coolsvg_go-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
