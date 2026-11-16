# github.com/unixpickle/model3d/fileformats — ASCII PLY / Go

Pinned release: `v0.4.23`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/go/github-com-unixpickle-model3d-fileformats/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply go github_com_unixpickle_model3d_fileformats
python3 parsarium.py run ascii_ply go github_com_unixpickle_model3d_fileformats controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply go github_com_unixpickle_model3d_fileformats CORPUS_DIR runs/ascii_ply-github_com_unixpickle_model3d_fileformats-replay
python3 parsarium.py afl build ascii_ply go github_com_unixpickle_model3d_fileformats
python3 parsarium.py afl prepare ascii_ply go github_com_unixpickle_model3d_fileformats runs/ascii_ply-github_com_unixpickle_model3d_fileformats-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
