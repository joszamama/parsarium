# github.com/fogleman/fauxgl — ASCII PLY / Go

Pinned release: `v0.0.0-20250110135958-abf826acbbbd`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/go/github-com-fogleman-fauxgl/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply go github_com_fogleman_fauxgl
python3 parsarium.py run ascii_ply go github_com_fogleman_fauxgl controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply go github_com_fogleman_fauxgl CORPUS_DIR runs/ascii_ply-github_com_fogleman_fauxgl-replay
python3 parsarium.py afl build ascii_ply go github_com_fogleman_fauxgl
python3 parsarium.py afl prepare ascii_ply go github_com_fogleman_fauxgl runs/ascii_ply-github_com_fogleman_fauxgl-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
