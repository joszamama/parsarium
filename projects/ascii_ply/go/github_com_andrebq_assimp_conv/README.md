# github.com/andrebq/assimp/conv — ASCII PLY / Go

Pinned release: `v0.0.0-20121130215243-a775ba6866d8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/go/github-com-andrebq-assimp-conv/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply go github_com_andrebq_assimp_conv
python3 parsarium.py run ascii_ply go github_com_andrebq_assimp_conv controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply go github_com_andrebq_assimp_conv CORPUS_DIR runs/ascii_ply-github_com_andrebq_assimp_conv-replay
python3 parsarium.py afl build ascii_ply go github_com_andrebq_assimp_conv
python3 parsarium.py afl prepare ascii_ply go github_com_andrebq_assimp_conv runs/ascii_ply-github_com_andrebq_assimp_conv-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
