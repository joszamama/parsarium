# C++ × ASCII PLY: verified parser ranking

20 verified third-party package paths; working goal 20, ceiling 30. Homebrew install-on-request counts cover 2025-11-13 through 2026-11-13 and measure broad formula adoption, not PLY-specific use. They are compared only within C++; packages without a comparable Homebrew metric remain unranked.

| Rank | Package | Pinned release | Homebrew requested installs (365d) | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [vtk](https://examples.vtk.org/site/Cxx/IO/ReadPLY/) | 9.7.2 | 11,283 | three vertices, one polygon and its three indices | VTK vtkPLYReader over bundled vtkPLY syntax parser |
| 2 | [assimp](https://github.com/assimp/assimp-docs/blob/master/source/usage/use_the_lib.rst) | 6.0.6 | 7,646 | three vertices and one triangular face from ASCII PLY | Assimp native PLY loader |
| 3 | [cgal](https://doc.cgal.org/latest/Surface_mesh/group__PkgSurfaceMeshIOFuncPLY.html) | 6.2.1 | 5,504 | three vertices and one face in a parsed Surface_mesh | CGAL Surface_mesh PLY reader |
| 4 | [pcl](https://pointclouds.org/documentation/classpcl_1_1_p_l_y_reader.html) | 1.15.1 | 1,697 | three vertices, one polygon and its three indices | PCL PLYReader native implementation |
| 5 | [geogram](https://github.com/BrunoLevy/geogram/wiki/Mesh) | 1.10.1 | 97 | three mesh vertices and one triangle facet with indices | Geogram over bundled RPly 1.1.4 |
| 6 | [open-mesh](https://www.graphics.rwth-aachen.de/media/openmesh_static/Documentations/OpenMesh-6.0-Documentation/a00740.html) | 11.0.0 | 66 | three vertices and one triangular face from ASCII PLY | OpenMesh PLYReader |
| unranked | [happly](https://github.com/nmwsharp/happly/blob/v1.1.0/README.md) | 1.1.0 | unknown | three parsed vertices and one triangular face from ASCII PLY | hapPLY header-only PLY parser |
| unranked | [tinyply](https://github.com/ddiakopoulos/tinyply/blob/3.0/README.md) | 3.0 | unknown | three parsed vertices and one triangular face from ASCII PLY | tinyply header-only PLY parser |
| unranked | [rply](https://w3.impa.br/~diego/software/rply/) | 1.1.4 | unknown | three vertex callbacks and three face-index callbacks from ASCII PLY | RPly 1.1.4 ANSI C parser |
| unranked | [libigl](https://libigl.github.io/dox/readPLY_8h.html) | 2.6.4 | unknown | three vertex positions and one triangle face matrix | libigl readPLY over bundled tinyply 2.3.2 |
| unranked | [plywoot](https://github.com/ton/PLYwoot/blob/v0.3.0/README.md) | 0.3.0 | unknown | vertices and face indices | PLYwoot native ASCII parser |
| unranked | [turboply](https://github.com/guangxi-research/turboply/blob/v1.0.6/README.md) | 1.0.6 | unknown | vertices and face indices | TurboPLY native reader |
| unranked | [vcglib](https://github.com/cnr-isti-vclab/vcglib/blob/2025.07/apps/sample/trimesh_attribute_ply/trimesh_attribute_ply.cpp) | 2025.07 | unknown | three vertices and a triangle face with indices | VCGlib native plylib parser |
| unranked | [trimesh2](https://github.com/Forceflow/trimesh2/blob/2022.03.04/README.md) | 2022.03.04 | unknown | three vertices and a triangle face with indices | TriMesh2 native PLY reader |
| unranked | [geometry-central](https://geometry-central.net/surface/utilities/simple_polygon_mesh/) | 1.1.0 | unknown | mesh vertices and polygon indices | Geometry Central over hapPLY |
| unranked | [AssetKit](https://github.com/recp/AssetKit/blob/v0.7.4/samples/read_meshes.c) | 0.7.4 | unknown | mesh vertices and parsed face indices | AssetKit native ASCII PLY importer |
| unranked | [rplycpp](https://github.com/manlito/rplycpp/blob/v1.1.0/README.md) | 1.1.0 | unknown | three vertices and a triangle face with indices | rplycpp over bundled RPly |
| unranked | [Easy3D](https://github.com/LiangliangNan/Easy3D/blob/v2.6.1/easy3d/fileio/surface_mesh_io.h) | 2.6.1 | unknown | three vertices and one triangle face with indices | Easy3D over bundled RPly 1.1.4 |
| unranked | [libpointmatcher](https://github.com/norlab-ulaval/libpointmatcher/blob/1.4.4/pointmatcher/IO.h) | 1.4.4 | unknown | three point vertices and coordinate sums | native libpointmatcher PLY parser |
| unranked | [meshio++](https://github.com/loumalouomega/meshioplusplus/blob/v20.0.0/src/cpp/include/meshioplusplus/formats/ply.hpp) | 20.0.0 | unknown | three vertices and one triangle face with indices | native meshio++ C++ PLY parser |

Assimp C and C++ APIs share one native loader. libigl exposes its own matrix API but bundles tinyply 2.3.2, while standalone tinyply is pinned at 3.0. Geometry Central wraps a pinned hapPLY submodule. TriMesh2 uses its native PLY reader and is a fork of Szymon Rusinkiewicz’s original TriMesh2. VCGlib ImporterPLY uses its bundled plylib implementation. PCL and VTK use separate PLY readers; VTK bundles vtkPLY. Formula-name hits are leads rather than parser proof. See `cell.json`, `leads.json`, `source-lock.json`, and `verification.json`.

AssetKit v0.7.4 was verified through its local `ak_load` API in both C and C++. Both adapters share one native PLY parser family. Its tagged source, five submodule commits, and adapter control results are pinned; a comparable Homebrew install-on-request count is unavailable.

rplycpp v1.1.0 parsed the valid ASCII triangle through its documented local-file C++ callback API. It bundles RPly, so its underlying parser family is shared with the standalone RPly path. Its Homebrew requested-install count is unavailable; miniply remains excluded because it has no tagged release to pin.

Geogram v1.10.1 parsed the triangle through `mesh_load`; its PLY handler uses bundled RPly 1.1.4. Its 97 Homebrew requested installs over the same 365-day window place it between PCL and OpenMesh in the recorded metric.

Easy3D v2.6.1 parsed the control through its `SurfaceMeshIO::load` mesh API. Its PLY implementation wraps bundled RPly 1.1.4; a comparable Homebrew requested-install count is unavailable.

libpointmatcher 1.4.4 parsed the three point vertices through its native PLY implementation and returned coordinate sums. Its point-cloud API does not return the control’s face. It has no comparable Homebrew requested-install count.

meshio++ v20.0.0 parsed the valid triangle through its documented C++ `read_ply` API and its own PLY implementation. The released code needs pinned LLVM 23.1.4 and explicit `<bit>` and `<cstdlib>` includes for the recorded macOS build. Its requested-install count is unavailable; its recent adoption is uncertain. The cell meets the 20-path working target, while unsearched projects and broader PLY layouts remain uncertain.
