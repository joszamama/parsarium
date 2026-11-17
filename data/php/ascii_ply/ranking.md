# PHP × ASCII PLY: selected parsers

3 control-verified third-party paths selected from 5 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

Packagist lifetime package downloads.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [magdev/php-assimp](https://github.com/magdev/php-assimp/blob/0.3.2/README.md) | 0.3.2 | 94 | One mesh with three vertices and one face reported from a valid local ASCII PLY triangle | Assimp native PLY loader through magdev/php-assimp CLI wrapper |

## Supplemental numeric evidence

These paths lack a positive primary metric. Their figures are reported separately and are not compared numerically with the table above.

| Supplemental rank | Package | Release | Signal | Value | Parsed scope | Parser family |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | [zelon88/hrconvert2](https://github.com/zelon88/HRConvert2/blob/v4.0.0/Resources/Pipelines/Model/pipelineConfig.php) | v4.0.0 | [GitHub upstream stars](https://github.com/zelon88/HRConvert2) | 1,397 | One valid ASCII PLY triangle converted through real PyMeshLab and Assimp stages; OBJ geometry and both stage outputs observed | HRConvert2 PHP Model pipeline over PyMeshLab PLY reader and Assimp exporter |
| 2 | [collectiveaccess/providence](https://github.com/collectiveaccess/providence/blob/2.0.12/app/lib/Parsers/PlyToStl.php) | 2.0.12 | [GitHub upstream stars](https://github.com/collectiveaccess/providence) | 389 | One valid ASCII PLY triangle; converted STL contains one parsed facet, three vertices and the second X coordinate | CollectiveAccess Providence native PHP PlyToStl |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
