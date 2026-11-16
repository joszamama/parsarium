# msh_ply — ASCII PLY / C

- **Pinned release:** `1.02`
- **License:** MIT OR Unlicense
- **Parsed scope:** ASCII PLY triangle: three parsed vertex coordinates and one face with final index 2
- **Underlying family:** msh_ply native single-header C reader
- **Local input API:** `msh_ply_open(local filename, "rb"); msh_ply_add_descriptor; msh_ply_read`
- **Documentation:** [API reference](<https://github.com/mhalber/msh/blob/eb1996102858ad467f68d087644759d84df21ca6/msh_ply.h>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_ply/parsers.json) · [control verification](../../../../data/c/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1,
  "second_x": 1.0,
  "last_index": 2
}
```

Standalone versioned header at a pinned upstream commit. It is a distinct reader from RPly/SPly and Assimp; its benchmark is project-authored and is not treated as a popularity metric.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/c/msh_ply/README.md)

```sh
python3 parsarium.py build ascii_ply c msh_ply
python3 parsarium.py run ascii_ply c msh_ply controls/ascii_ply/triangle.ply
```

**Coverage limit:** The base libFuzzer valid control returns expected fields while UBSan reports misaligned int32_t accesses in upstream msh_ply.h lines 1436 and 969. The AFL++ valid control trapped with alignment checks enabled, so its build adds -fno-sanitize=alignment while retaining AddressSanitizer and other UBSan checks.
