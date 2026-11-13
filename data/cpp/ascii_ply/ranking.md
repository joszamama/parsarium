# C++ × ASCII PLY: verified parser ranking

6 verified third-party package paths; working goal 20, ceiling 30. Homebrew install-on-request counts cover 2025-11-13 through 2026-11-13 and measure broad formula adoption, not PLY-specific use. They are compared only within C++; header-only releases without a Homebrew metric remain unranked.

| Rank | Package | Pinned release | Homebrew requested installs (365d) | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [Assimp](https://github.com/assimp/assimp-docs/blob/master/source/usage/use_the_lib.rst) | 6.0.6 | 7,646 | three vertices, one face | Assimp native PLY loader |
| 2 | [CGAL](https://doc.cgal.org/latest/Surface_mesh/group__PkgSurfaceMeshIOFuncPLY.html) | 6.2.1 | 5,504 | three vertices, one face | CGAL Surface_mesh PLY reader |
| 3 | [OpenMesh](https://www.graphics.rwth-aachen.de/media/openmesh_static/Documentations/OpenMesh-6.0-Documentation/a00740.html) | 11.0.0 | 66 | three vertices, one face | OpenMesh PLYReader |
| unranked | [RPly](https://w3.impa.br/~diego/software/rply/) | 1.1.4 | unknown | vertex and face-index callbacks | RPly ANSI C parser |
| unranked | [hapPLY](https://github.com/nmwsharp/happly/blob/v1.1.0/README.md) | 1.1.0 | unknown | vertices and face indices | hapPLY header-only parser |
| unranked | [tinyply](https://github.com/ddiakopoulos/tinyply/blob/3.0/README.md) | 3.0 | unknown | three vertices, one face | tinyply header-only parser |

Assimp C and C++ APIs share one PLY loader; CGAL, OpenMesh, hapPLY, tinyply and RPly have distinct parsers. Formula-name hits are leads rather than parser proof. See `cell.json`, `leads.json`, `source-lock.json`, and `verification.json`.
