# CPP × ASCII PLY: selected parsers

10 control-verified third-party paths selected from 21 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

Homebrew install-on-request count over 365 days.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [vtk](https://examples.vtk.org/site/Cxx/IO/ReadPLY/) | 9.7.2 | 11,283 | three vertices, one polygon and its three indices | VTK vtkPLYReader over bundled vtkPLY syntax parser |
| 2 | [assimp](https://github.com/assimp/assimp-docs/blob/master/source/usage/use_the_lib.rst) | 6.0.6 | 7,646 | three vertices and one triangular face from ASCII PLY | Assimp native PLY loader |
| 3 | [cgal](https://doc.cgal.org/latest/Surface_mesh/group__PkgSurfaceMeshIOFuncPLY.html) | 6.2.1 | 5,504 | three vertices and one face in a parsed Surface_mesh | CGAL Surface_mesh PLY reader |
| 4 | [pcl](https://pointclouds.org/documentation/classpcl_1_1_p_l_y_reader.html) | 1.15.1 | 1,697 | three vertices, one polygon and its three indices | PCL PLYReader native implementation |
| 5 | [f3d](https://github.com/f3d-app/f3d/blob/v4.0.1/library/public/scene.h) | 4.0.1 | 1,516 | ASCII triangle produced three parsed points and one cell | F3D native PLY plugin over VTK vtkPLYReader |
| 6 | [geogram](https://github.com/BrunoLevy/geogram/wiki/Mesh) | 1.10.1 | 97 | three parsed mesh vertices and one triangle facet with indices | Geogram PLYIOHandler over bundled RPly 1.1.4 |
| 7 | [open-mesh](https://www.graphics.rwth-aachen.de/media/openmesh_static/Documentations/OpenMesh-6.0-Documentation/a00740.html) | 11.0.0 | 66 | three vertices and one triangular face from ASCII PLY | OpenMesh PLYReader |

## Supplemental numeric evidence

These paths lack a positive primary metric. Their figures are reported separately and are not compared numerically with the table above.

| Supplemental rank | Package | Release | Signal | Value | Parsed scope | Parser family |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | [libigl](https://libigl.github.io/dox/readPLY_8h.html) | 2.6.4 | [GitHub upstream stars](https://github.com/libigl/libigl) | 5,127 | three vertex positions and one triangle face matrix | libigl readPLY over bundled tinyply 2.3.2 |
| 2 | [libpointmatcher](https://github.com/norlab-ulaval/libpointmatcher/blob/1.4.4/pointmatcher/IO.h) | 1.4.4 | [GitHub upstream stars](https://github.com/norlab-ulaval/libpointmatcher) | 1,845 | three parsed point-cloud vertices with x/y/z coordinate sums from ASCII PLY | libpointmatcher native PLY point-cloud parser |
| 3 | [easy3d](https://github.com/LiangliangNan/Easy3D/blob/v2.6.1/easy3d/fileio/surface_mesh_io.h) | 2.6.1 | [GitHub upstream stars](https://github.com/LiangliangNan/Easy3D) | 1,660 | three mesh vertices and one triangle face with indices from ASCII PLY | Easy3D PLY reader over bundled RPly 1.1.4 |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
