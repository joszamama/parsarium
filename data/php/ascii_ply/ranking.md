# PHP × ASCII PLY: verified parser ranking

Three verified third-party package paths; working goal 20, ceiling 30. Seventeen paths remain below the goal. The within-PHP primary metric is Packagist lifetime downloads across all releases, observed on 2026-11-14. It measures package adoption, not PLY-specific use. Only one path has this metric, so the three cannot be ordered as a most-used top three.

| Rank | Package | Pinned release | Packagist lifetime downloads | Verified scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [magdev/php-assimp](https://github.com/magdev/php-assimp/tree/0.3.2) | 0.3.2 | 94 | one mesh, three vertices, one face | Assimp 6.0.6 native PLY importer through PHP CLI wrapper |
| unranked | [collectiveaccess/providence](https://github.com/collectiveaccess/providence/tree/2.0.12) | 2.0.12 | unavailable | local PLY vertex and face rows converted to one STL facet with three vertices | Providence native PHP PlyToStl |
| unranked | [ahg/3d-model](https://github.com/ArchiveHeritageGroup/heratio/tree/v1.165.35/packages/ahg-3d-model) | 1.165.35 | unavailable | PLY header declares three vertices and one face; body geometry was not parsed | Heratio pure PHP metadata extractor |

Providence exposes a parser class in its released `app/lib/Parsers` directory. Its public `PlyToStl::convert` API read the valid local triangle and produced format-aware geometry. The standalone adapter supplies a no-op `Db.php` file for an unused legacy include, so it does not test the full application. Heratio's released `ahg/3d-model` Composer library uses `ModelMetadataExtractor::extract` to read PLY header element counts. This verifies a narrower parser scope than geometry loading. The Assimp wrapper is a distinct PHP package path that shares its underlying native parser with other ecosystem cells. Its later 0.6.0 release remains excluded after a failed control.

Packagist returned no package entries for Providence or `ahg/3d-model` on the observation date. Their GitHub stars are recorded as auxiliary repository signals only. Copied Providence `PlyToStl.php` files found in code search are not separate verified packages.

The bounded searches saved 267 hits with 254 unique identifiers across Packagist, GitHub repository search, GitHub code search, and Sourcegraph. The `element face` GitHub code query reported 204 matches; only its first 100 are in the saved window. The searches do not establish that no other PHP PLY parser exists. The PHP standard and bundled API inventory found no documented format-aware PLY parser within its stated scope. Evidence and limits are in `cell.json`, `supplementary-search.json`, `leads.json`, `source-lock.json`, `verification.json`, and `standard.json`.
