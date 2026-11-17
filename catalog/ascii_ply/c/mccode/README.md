# mccode — ASCII PLY / C

- **Pinned release:** `3.10.2`
- **License:** GPL-3.0
- **Parsed scope:** One valid ASCII PLY triangle; C runtime parsed three vertices and one polygon and computed 1.0 by 1.0 bounding box
- **Underlying family:** McCode native C OFF/PLY parser (interoff-lib)
- **Local input API:** `McStas Guide_anyshape(geometry=local ASCII PLY path) component parameter; generated C calls off_init into off_struct`
- **Documentation:** [API reference](<https://github.com/mccode-dev/McCode/blob/v3.10.2/mcstas-comps/optics/Guide_anyshape.comp>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_ply/parsers.json) · [control verification](../../../../data/c/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1,
  "length": 1.0,
  "width": 1.0
}
```

McStas component library compiles the tagged C interoff-lib parser into an instrument. It is a distinct engine. The 80-artifact conda environment and installed parser sources are pinned; only geometry initialization is tested, not neutron simulation.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/c/mccode/README.md)

```sh
python3 parsarium.py build ascii_ply c mccode
python3 parsarium.py run ascii_ply c mccode controls/ascii_ply/triangle.ply
```

**Coverage limit:** McCode 3.10.2 rejects valid zero-face PLY point clouds; this path accepts polygonal meshes with at least one face. The upstream parser can exit on rejected input, so execution is one file per process.
