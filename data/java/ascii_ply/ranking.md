# Java × ASCII PLY: verified parser ranking

Five verified third-party Maven package paths; working goal 20, ceiling 30. The metric is deps.dev's known public direct dependents for each exact release, a limited within-Java adoption proxy. It does not measure PLY-specific use, and zero can reflect coverage or version-age gaps. LWJGL Assimp shares the native Assimp PLY parser family with the C++ Assimp path.

| Rank | Package | Pinned release | Direct dependents | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [LWJGL Assimp](https://javadoc.lwjgl.org/org/lwjgl/assimp/Assimp.html) | org.lwjgl:lwjgl-assimp:3.4.3 | 13 | ASCII triangle vertices, face and indices | LWJGL binding over native Assimp PLY importer |
| 2 | [jPLY](https://github.com/smurn/jPLY) | org.smurn:jply:0.2.0 | 0 | ASCII triangle vertices, face and indices | jPLY native PLY element reader |
| 2 | [MeshIO](https://github.com/NathanJAdams/MeshIO#using-formats-directly) | com.ripplargames:meshio:2.1.2 | 0 | ASCII triangle vertices, face and indices | MeshIO native ASCII PLY mesh reader |
| 2 | [mesh-ply](https://github.com/kazocsaba/mesh-ply/blob/mesh-ply-1.1.0/src/main/java/hu/kazocsaba/v3d/mesh/format/ply/PlyReader.java) | hu.kazocsaba.geom3d:mesh-ply:1.1.0 | 0 | ASCII triangle vertices, face and indices | kazocsaba mesh-ply native PLY reader |
| 2 | [pcutil](https://github.com/zhoujianling/PointCloudUtilities#plyreader) | cn.jimmiez:pcutil:0.3.0 | 0 | ASCII triangle vertices, face and indices | PointCloudUtilities annotated PLY reader |

Four bounded Maven search queries saved six name hits; two queries timed out. The Java standard library has no documented PLY parser. The Ardor3D lead remains unresolved. See `cell.json`, `registry-snapshot.json`, `leads.json`, `standard.json`, and `verification.json`.
