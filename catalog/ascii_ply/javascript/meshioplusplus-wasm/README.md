# @meshioplusplus/wasm — ASCII PLY / JavaScript

- **Pinned release:** `20.0.0`
- **Upstream:** [source repository](<https://github.com/loumalouomega/meshioplusplus>) · [npm](<https://www.npmjs.com/package/@meshioplusplus/wasm>)
- **License:** MIT AND (LGPL-2.1-only WITH OCCT-exception-1.0) AND LGPL-2.1-only AND LGPL-3.0-or-later
- **Parsed scope:** triangle mesh
- **Underlying family:** meshio++ WASM
- **Local input API:** `FS.writeFile(localVirtualPath, bytes); readMesh(localVirtualPath)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@meshioplusplus/wasm>)
- **Catalog evidence:** [parser record](../../../../data/javascript/ascii_ply/parsers.json) · [control verification](../../../../data/javascript/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/javascript/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": [
    [
      0,
      0,
      0
    ],
    [
      1,
      0,
      0
    ],
    [
      0,
      1,
      0
    ]
  ],
  "faces": [
    [
      0,
      1,
      2
    ]
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/javascript/meshioplusplus_wasm/README.md)

```sh
python3 parsarium.py build ascii_ply javascript meshioplusplus_wasm
python3 parsarium.py run ascii_ply javascript meshioplusplus_wasm controls/ascii_ply/triangle.ply
```
