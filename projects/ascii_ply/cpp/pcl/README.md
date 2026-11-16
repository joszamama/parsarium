# pcl — ASCII PLY / C++

Pinned release: `1.15.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/cpp/pcl/README.md)

The replay reports the parsed vertex count, polygon count, and the full index list of the first polygon. For a point cloud without polygons, `face` is empty.

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply cpp pcl
python3 parsarium.py run ascii_ply cpp pcl controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply cpp pcl CORPUS_DIR runs/ascii_ply-pcl-replay
python3 parsarium.py afl build ascii_ply cpp pcl
python3 parsarium.py afl prepare ascii_ply cpp pcl runs/ascii_ply-pcl-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
