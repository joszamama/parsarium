# C × ASCII PLY: selected parsers

9 control-verified third-party paths selected from 21 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

Homebrew install-on-request count over 365 days.

| Rank | Package | Release | Homebrew installs (365 days) | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [assimp](https://github.com/assimp/assimp-docs/blob/master/source/usage/use_the_lib.rst) | 6.0.6 | 7,672 | three vertices and one triangular face from ASCII PLY | Assimp native PLY loader |
| 2 | [gmsh](https://gmsh.info/doc/texinfo/gmsh.html) | 4.15.2 | 1,666 | One valid local ASCII PLY triangle; three parsed positions, one triangle and three node references through the C API | Gmsh native PLY reader |
| 3 | [f3d](https://github.com/f3d-app/f3d/blob/v4.0.1/c/scene_c_api.h) | 4.0.1 | 1,521 | ASCII triangle produced three parsed points and one cell | F3D native PLY plugin over VTK vtkPLYReader |

## Supplemental numeric evidence

These paths lack a positive primary metric. Their figures are reported separately and are not compared numerically with the table above.

| Supplemental rank | Package | Release | Signal | Value | Parsed scope | Parser family |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | [stereokit](https://stereokit.net/Pages/StereoKit/Model.html) | v0.3.11 | [GitHub stars](https://github.com/StereoKit/StereoKit) | 1,093 | One valid ASCII PLY triangle through the full native C ABI in offscreen Mesa mode; vertices and face indices observed | StereoKit model PLY loader over bundled micro_ply |
| 2 | [brlcad](https://brlcad.org/docs/html/articles/gcv.html) | 7.46.0 | [GitHub stars](https://github.com/BRL-CAD/brlcad) | 1,045 | three vertices, one face, triangle indices and BRL-CAD default scaled coordinate from local ASCII PLY | BRL-CAD gcv-ply plugin over bundled RPly 1.1.4 |
| 3 | [libagar](https://github.com/JulNadeauCA/libagar/blob/release-1.7.1/sg/SG_Object.3) | 1.7.1 | [GitHub stars](https://github.com/JulNadeauCA/libagar) | 465 | three vertices and one triangular facet with parsed vertex ids from ASCII PLY | Agar-SG native PLY loader (sg/sg_load_ply.c) |
| 4 | [assetkit](https://github.com/recp/AssetKit/blob/v0.7.4/samples/read_meshes.c) | 0.7.4 | [GitHub stars](https://github.com/recp/AssetKit) | 217 | three vertices and one triangular face with parsed indices from ASCII PLY | AssetKit native ASCII PLY importer |
| 5 | [mdal](https://github.com/lutraconsulting/MDAL/blob/release-1.3.3/mdal/api/mdal.h) | 1.3.3 | [GitHub stars](https://github.com/lutraconsulting/MDAL) | 190 | Three parsed vertices, one face and face indices | MDAL PLY driver over bundled libplyxx |
| 6 | [mccode](https://github.com/mccode-dev/McCode/blob/v3.10.2/mcstas-comps/optics/Guide_anyshape.comp) | 3.10.2 | [GitHub stars](https://github.com/mccode-dev/McCode) | 100 | One valid ASCII PLY triangle; C runtime parsed three vertices and one polygon and computed 1.0 by 1.0 bounding box | McCode native C OFF/PLY parser (interoff-lib) |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
