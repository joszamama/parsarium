# Open3D — ASCII PLY / Python

Pinned release: `0.20.0`. [Manifest](manifest.json) · [verification receipt](verification.json) · [catalog API and parser-family evidence](../../../../catalog/ascii_ply/python/open3d/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply python open3d
python3 parsarium.py run ascii_ply python open3d controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply python open3d CORPUS_DIR runs/ascii_ply-open3d-replay
python3 parsarium.py afl build ascii_ply python open3d
python3 parsarium.py afl prepare ascii_ply python open3d runs/ascii_ply-open3d-afl --timeout-ms 180000
```

The valid ASCII PLY control produces three vertices and one triangle, with first vertex `(0, 0, 0)` and last vertex `(0, 1, 0)`. Replace `CORPUS_DIR` with a directory of PLY files. `afl prepare` creates a seeded run; it does not start a campaign.

**Feedback:** AFL++ QEMU observes native binary edges in Open3D's exported `ReadTriangleMeshFromPLY` function. [The smoke check](binary-feedback/README.md) demonstrates stable and input-sensitive feedback. The wheel does not include instrumented PLY parser source, so the receipt reports no source-line coverage.
