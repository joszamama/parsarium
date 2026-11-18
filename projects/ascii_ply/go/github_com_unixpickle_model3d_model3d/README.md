# github.com/unixpickle/model3d/model3d — ASCII PLY / Go

Pinned release: `v0.4.23`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/go/github-com-unixpickle-model3d-model3d/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply go github_com_unixpickle_model3d_model3d
python3 parsarium.py run ascii_ply go github_com_unixpickle_model3d_model3d controls/ascii_ply/triangle-vertex-index.ply
python3 parsarium.py replay ascii_ply go github_com_unixpickle_model3d_model3d CORPUS_DIR runs/ascii_ply-github_com_unixpickle_model3d_model3d-replay
python3 parsarium.py afl build ascii_ply go github_com_unixpickle_model3d_model3d
python3 parsarium.py afl prepare ascii_ply go github_com_unixpickle_model3d_model3d runs/ascii_ply-github_com_unixpickle_model3d_model3d-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
