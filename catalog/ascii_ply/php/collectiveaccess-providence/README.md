# collectiveaccess/providence — ASCII PLY / PHP

- **Pinned release:** `2.0.12`
- **Upstream:** [source repository](<https://github.com/collectiveaccess/providence>) · [Packagist](<https://packagist.org/packages/collectiveaccess/providence>)
- **License:** GPL-3.0
- **Parsed scope:** One valid ASCII PLY triangle; converted STL contains one parsed facet, three vertices and the second X coordinate
- **Underlying family:** CollectiveAccess Providence native PHP PlyToStl
- **Local input API:** `PlyToStl::convert(local ASCII PLY path, local STL output path); parses vertex coordinates and face indices`
- **Documentation:** [API reference](<https://github.com/collectiveaccess/providence/blob/2.0.12/app/lib/Parsers/PlyToStl.php>)
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

Providence exposes a PHP parser class in app/lib/Parsers. Its conversion path reads PLY vertex and face rows; the adapter supplies a no-op file for an unused Db.php include. Search hits containing copied PlyToStl.php files are not counted as separate packages without independent release and API verification.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/php/providence/README.md)

```sh
python3 parsarium.py build ascii_ply php providence
python3 parsarium.py run ascii_ply php providence controls/ascii_ply/triangle.ply
```
