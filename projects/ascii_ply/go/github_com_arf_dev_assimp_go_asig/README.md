# github.com/ARF-DEV/assimp-go/asig — ASCII PLY / Go

Pinned release: `v0.0.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/go/github-com-arf-dev-assimp-go-asig/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply go github_com_arf_dev_assimp_go_asig
python3 parsarium.py run ascii_ply go github_com_arf_dev_assimp_go_asig controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply go github_com_arf_dev_assimp_go_asig CORPUS_DIR runs/ascii_ply-github_com_arf_dev_assimp_go_asig-replay
python3 parsarium.py afl build ascii_ply go github_com_arf_dev_assimp_go_asig
python3 parsarium.py afl prepare ascii_ply go github_com_arf_dev_assimp_go_asig runs/ascii_ply-github_com_arf_dev_assimp_go_asig-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
