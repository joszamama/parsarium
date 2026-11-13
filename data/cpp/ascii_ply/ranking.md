# C++ × ASCII PLY: verified parser ranking

11 verified third-party package paths; working goal 20, ceiling 30. Homebrew install-on-request counts cover 2025-11-13 through 2026-11-13 and measure broad formula adoption, not PLY-specific use. They are compared only within C++; packages without a comparable Homebrew metric remain unranked.

| Rank | Package | Pinned release | Homebrew requested installs (365d) | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [vtk](https://examples.vtk.org/site/Cxx/IO/ReadPLY/) | 9.7.2 | 11,283 | three vertices, one polygon and its three indices | VTK vtkPLYReader over bundled vtkPLY syntax parser |
| 2 | [assimp](https://github.com/assimp/assimp-docs/blob/master/source/usage/use_the_lib.rst) | 6.0.6 | 7,646 | three vertices and one triangular face from ASCII PLY | Assimp native PLY loader |
| 3 | [cgal](https://doc.cgal.org/latest/Surface_mesh/group__PkgSurfaceMeshIOFuncPLY.html) | 6.2.1 | 5,504 | three vertices and one face in a parsed Surface_mesh | CGAL Surface_mesh PLY reader |
| 4 | [pcl](https://pointclouds.org/documentation/classpcl_1_1_p_l_y_reader.html) | 1.15.1 | 1,697 | three vertices, one polygon and its three indices | PCL PLYReader native implementation |
| 5 | [open-mesh](https://www.graphics.rwth-aachen.de/media/openmesh_static/Documentations/OpenMesh-6.0-Documentation/a00740.html) | 11.0.0 | 66 | three vertices and one triangular face from ASCII PLY | OpenMesh PLYReader |
| unranked | [happly](https://github.com/nmwsharp/happly/blob/v1.1.0/README.md) | 1.1.0 | unknown | three parsed vertices and one triangular face from ASCII PLY | hapPLY header-only PLY parser |
| unranked | [tinyply](https://github.com/ddiakopoulos/tinyply/blob/3.0/README.md) | 3.0 | unknown | three parsed vertices and one triangular face from ASCII PLY | tinyply header-only PLY parser |
| unranked | [rply](https://w3.impa.br/~diego/software/rply/) | 1.1.4 | unknown | three vertex callbacks and three face-index callbacks from ASCII PLY | RPly 1.1.4 ANSI C parser |
| unranked | [libigl](https://libigl.github.io/dox/readPLY_8h.html) | 2.6.4 | unknown | three vertex positions and one triangle face matrix | libigl readPLY over bundled tinyply 2.3.2 |
| unranked | [plywoot](https://github.com/ton/PLYwoot/blob/v0.3.0/README.md) | 0.3.0 | unknown | vertices and face indices | PLYwoot native ASCII parser |
| unranked | [turboply](https://github.com/guangxi-research/turboply/blob/v1.0.6/README.md) | 1.0.6 | unknown | vertices and face indices | TurboPLY native reader |

Assimp C and C++ APIs share one native loader. libigl exposes its own matrix API but bundles tinyply 2.3.2, while standalone tinyply is pinned at 3.0. PCL and VTK use separate PLY readers; VTK bundles vtkPLY. Formula-name hits are leads rather than parser proof. See `cell.json`, `leads.json`, `source-lock.json`, and `verification.json`.
