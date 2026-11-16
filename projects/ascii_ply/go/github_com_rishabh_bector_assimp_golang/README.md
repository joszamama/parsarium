# github.com/rishabh-bector/assimp-golang — ASCII PLY / Go

Pinned release: `v0.0.0-20190130041627-cbac4dcfdaf3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/go/github-com-rishabh-bector-assimp-golang/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply go github_com_rishabh_bector_assimp_golang
python3 parsarium.py run ascii_ply go github_com_rishabh_bector_assimp_golang controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply go github_com_rishabh_bector_assimp_golang CORPUS_DIR runs/ascii_ply-github_com_rishabh_bector_assimp_golang-replay
python3 parsarium.py afl build ascii_ply go github_com_rishabh_bector_assimp_golang
python3 parsarium.py afl prepare ascii_ply go github_com_rishabh_bector_assimp_golang runs/ascii_ply-github_com_rishabh_bector_assimp_golang-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
