# github.com/rm4n0s/glutter/model/ply — ASCII PLY / Go

Pinned release: `v1.17.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/go/github-com-rm4n0s-glutter-model-ply/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply go github_com_rm4n0s_glutter_model_ply
python3 parsarium.py run ascii_ply go github_com_rm4n0s_glutter_model_ply controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply go github_com_rm4n0s_glutter_model_ply CORPUS_DIR runs/ascii_ply-github_com_rm4n0s_glutter_model_ply-replay
python3 parsarium.py afl build ascii_ply go github_com_rm4n0s_glutter_model_ply
python3 parsarium.py afl prepare ascii_ply go github_com_rm4n0s_glutter_model_ply runs/ascii_ply-github_com_rm4n0s_glutter_model_ply-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
