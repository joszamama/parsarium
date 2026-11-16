# github.com/ajermaky/assimp-go/v2/asig — ASCII PLY / Go

Pinned release: `v2.0.0-20240713211439-0860f3b5f93c`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/go/github-com-ajermaky-assimp-go-v2-asig/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply go github_com_ajermaky_assimp_go_v2_asig
python3 parsarium.py run ascii_ply go github_com_ajermaky_assimp_go_v2_asig controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply go github_com_ajermaky_assimp_go_v2_asig CORPUS_DIR runs/ascii_ply-github_com_ajermaky_assimp_go_v2_asig-replay
python3 parsarium.py afl build ascii_ply go github_com_ajermaky_assimp_go_v2_asig
python3 parsarium.py afl prepare ascii_ply go github_com_ajermaky_assimp_go_v2_asig runs/ascii_ply-github_com_ajermaky_assimp_go_v2_asig-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
