# github.com/tbogdala/assimp-go — ASCII PLY / Go

Pinned release: `v0.0.0-20160907223021-d10e2135f9fe`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/go/github-com-tbogdala-assimp-go/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply go github_com_tbogdala_assimp_go
python3 parsarium.py run ascii_ply go github_com_tbogdala_assimp_go controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply go github_com_tbogdala_assimp_go CORPUS_DIR runs/ascii_ply-github_com_tbogdala_assimp_go-replay
python3 parsarium.py afl build ascii_ply go github_com_tbogdala_assimp_go
python3 parsarium.py afl prepare ascii_ply go github_com_tbogdala_assimp_go runs/ascii_ply-github_com_tbogdala_assimp_go-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
