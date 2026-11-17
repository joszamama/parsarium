# go.viam.com/rdk/spatialmath — ASCII PLY / Go

Pinned release: `v1.17.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/go/go-viam-com-rdk-spatialmath/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply go go_viam_com_rdk_spatialmath
python3 parsarium.py run ascii_ply go go_viam_com_rdk_spatialmath controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply go go_viam_com_rdk_spatialmath CORPUS_DIR runs/ascii_ply-go_viam_com_rdk_spatialmath-replay
python3 parsarium.py afl build ascii_ply go go_viam_com_rdk_spatialmath
python3 parsarium.py afl prepare ascii_ply go go_viam_com_rdk_spatialmath runs/ascii_ply-go_viam_com_rdk_spatialmath-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
