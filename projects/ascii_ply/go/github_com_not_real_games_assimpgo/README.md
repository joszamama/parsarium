# github.com/NOT-REAL-GAMES/assimpgo — ASCII PLY / Go

Pinned release: `v0.0.0-20260306134222-05660fb62c9d`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/go/github-com-not-real-games-assimpgo/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply go github_com_not_real_games_assimpgo
python3 parsarium.py run ascii_ply go github_com_not_real_games_assimpgo controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply go github_com_not_real_games_assimpgo CORPUS_DIR runs/ascii_ply-github_com_not_real_games_assimpgo-replay
python3 parsarium.py afl build ascii_ply go github_com_not_real_games_assimpgo
python3 parsarium.py afl prepare ascii_ply go github_com_not_real_games_assimpgo runs/ascii_ply-github_com_not_real_games_assimpgo-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
