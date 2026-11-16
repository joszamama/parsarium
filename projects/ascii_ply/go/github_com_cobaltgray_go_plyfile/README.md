# github.com/cobaltgray/go-plyfile — ASCII PLY / Go

Pinned release: `v0.0.0-20210513130740-b21b0efca069`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/go/github-com-cobaltgray-go-plyfile/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply go github_com_cobaltgray_go_plyfile
python3 parsarium.py run ascii_ply go github_com_cobaltgray_go_plyfile controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply go github_com_cobaltgray_go_plyfile CORPUS_DIR runs/ascii_ply-github_com_cobaltgray_go_plyfile-replay
python3 parsarium.py afl build ascii_ply go github_com_cobaltgray_go_plyfile
python3 parsarium.py afl prepare ascii_ply go github_com_cobaltgray_go_plyfile runs/ascii_ply-github_com_cobaltgray_go_plyfile-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
