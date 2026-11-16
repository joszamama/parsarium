# collectiveaccess/pawtucket2 — ASCII PLY / PHP

- **Pinned release:** `2.0.12`
- **License:** GPL-3.0
- **Parsed scope:** One valid ASCII PLY triangle; converted STL contains one facet, three vertices and the second X coordinate
- **Underlying family:** CollectiveAccess native PHP PlyToStl shared with Providence
- **Local input API:** `PlyToStl::convert(local ASCII PLY path, local STL output path); parses vertex coordinates and face indices`
- **Documentation:** [API reference](<https://github.com/collectiveaccess/pawtucket2/blob/2.0.12/app/lib/Parsers/PlyToStl.php>)
- **Catalog evidence:** [parser record](../../../../data/php/ascii_ply/parsers.json) · [control verification](../../../../data/php/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/php/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "facets": 1,
  "vertices": 3,
  "second_x": 1.0
}
```

Separately tagged Pawtucket2 application distribution; its 2.0.12 parser file is byte-identical to Providence 2.0.12. The shared adapter supplies a no-op file for an unused Db.php include. These are distinct package paths but only one source-level parser engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/php/collectiveaccess_pawtucket2/README.md)

```sh
python3 parsarium.py build ascii_ply php collectiveaccess_pawtucket2
python3 parsarium.py run ascii_ply php collectiveaccess_pawtucket2 controls/ascii_ply/triangle.ply
```
