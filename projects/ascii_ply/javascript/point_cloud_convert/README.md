# point-cloud-convert — ASCII PLY / JavaScript

Pinned release: `0.0.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/javascript/point-cloud-convert/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply javascript point_cloud_convert
python3 parsarium.py run ascii_ply javascript point_cloud_convert controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply javascript point_cloud_convert CORPUS_DIR runs/ascii_ply-point_cloud_convert-replay
python3 parsarium.py afl build ascii_ply javascript point_cloud_convert
python3 parsarium.py afl prepare ascii_ply javascript point_cloud_convert runs/ascii_ply-point_cloud_convert-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
