# github.com/thebanri/limoni/graphics — ASCII PLY / Go

Pinned release: `v0.16.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/go/github-com-thebanri-limoni-graphics/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply go github_com_thebanri_limoni_graphics
python3 parsarium.py run ascii_ply go github_com_thebanri_limoni_graphics controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply go github_com_thebanri_limoni_graphics CORPUS_DIR runs/ascii_ply-github_com_thebanri_limoni_graphics-replay
python3 parsarium.py afl build ascii_ply go github_com_thebanri_limoni_graphics
python3 parsarium.py afl prepare ascii_ply go github_com_thebanri_limoni_graphics runs/ascii_ply-github_com_thebanri_limoni_graphics-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
