# nimbleterminal.dev/nt3d/mesh — ASCII PLY / Go

Pinned release: `v0.8.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/go/nimbleterminal-dev-nt3d-mesh/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply go nimbleterminal_dev_nt3d_mesh
python3 parsarium.py run ascii_ply go nimbleterminal_dev_nt3d_mesh controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply go nimbleterminal_dev_nt3d_mesh CORPUS_DIR runs/ascii_ply-nimbleterminal_dev_nt3d_mesh-replay
python3 parsarium.py afl build ascii_ply go nimbleterminal_dev_nt3d_mesh
python3 parsarium.py afl prepare ascii_ply go nimbleterminal_dev_nt3d_mesh runs/ascii_ply-nimbleterminal_dev_nt3d_mesh-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
