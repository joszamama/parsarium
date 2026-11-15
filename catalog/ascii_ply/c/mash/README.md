# mash — ASCII PLY / C

- **Pinned release:** `0.2.0`
- **License:** LGPL-2.1-or-later; bundled RPly MIT
- **Parsed scope:** One valid ASCII PLY triangle; tagged C loader and bundled RPly with graphics upload observed through stand-ins
- **Underlying family:** Mash PLY loader over bundled RPly 1.01
- **Local input API:** `mash_data_new(); mash_data_load(data, MASH_DATA_NONE, local .ply filename, GError**); mash_data_get_extents`
- **Documentation:** [API reference](<https://github.com/clutter-project/mash/blob/0.2.0/mash/mash-data.h>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_ply/parsers.json) · [control verification](../../../../data/c/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "indices": 3,
  "face": [
    0,
    1,
    2
  ],
  "second_x": 1.0,
  "min_x": 0.0,
  "max_x": 1.0
}
```

Separate released LGPL C package, sharing RPly parser lineage with Rig, BRL-CAD and the RPly package. The tagged MASH_TYPE_DATA_LOADER header has a type alias typo corrected by preinclude during this control; full Clutter rendering is not verified.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
