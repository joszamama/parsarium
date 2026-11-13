# Java × ASCII PLY: verified parser ranking

Eight verified third-party package paths: seven Maven artifacts and one source-built binding; working goal 20, ceiling 30. The metric is deps.dev's known public direct dependents for each exact Maven release, a limited within-Java adoption proxy. It does not measure PLY-specific use, and zero can reflect coverage or version-age gaps. LWJGL Assimp and MonkeyWrench share the native Assimp PLY parser family with the C++ Assimp path.

| Rank | Package | Pinned release | Direct dependents | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [LWJGL Assimp](https://javadoc.lwjgl.org/org/lwjgl/assimp/Assimp.html) | org.lwjgl:lwjgl-assimp:3.4.3 | 13 | ASCII triangle vertices, face and indices | LWJGL binding over native Assimp PLY importer |
| 2 | [jPLY](https://github.com/smurn/jPLY) | org.smurn:jply:0.2.0 | 0 | ASCII triangle vertices, face and indices | jPLY native PLY element reader |
| 2 | [MeshIO](https://github.com/NathanJAdams/MeshIO#using-formats-directly) | com.ripplargames:meshio:2.1.2 | 0 | ASCII triangle vertices, face and indices | MeshIO native ASCII PLY mesh reader |
| 2 | [mesh-ply](https://github.com/kazocsaba/mesh-ply/blob/mesh-ply-1.1.0/src/main/java/hu/kazocsaba/v3d/mesh/format/ply/PlyReader.java) | hu.kazocsaba.geom3d:mesh-ply:1.1.0 | 0 | ASCII triangle vertices, face and indices | kazocsaba mesh-ply native PLY reader |
| 2 | [pcutil](https://github.com/zhoujianling/PointCloudUtilities#plyreader) | cn.jimmiez:pcutil:0.3.0 | 0 | ASCII triangle vertices, face and indices | PointCloudUtilities annotated PLY reader |
| 2 | [MonkeyWrench](https://github.com/stephengold/MonkeyWrench#how-to-add-monkeywrench-to-an-existing-project) | com.github.stephengold:MonkeyWrench:1.0.1 | 0 | ASCII triangle vertices, face and indices | JMonkeyEngine wrapper over LWJGL Assimp PLY importer |
| 2 | [JavaGL Ply](https://github.com/javagl/Ply/tree/ply-parent-0.0.4) | de.javagl:ply:0.0.4 | 0 | ASCII triangle vertices, face and indices | JavaGL native Java PLY reader |
| unranked | [F3D Java binding](https://github.com/f3d-app/f3d/blob/v4.0.1/java/Scene.java) | 4.0.1 source release | unknown | one loaded file, one actor, three points, one cell | F3D native PLY plugin over VTK vtkPLYReader |

Four bounded Maven search queries saved seven name hits; prior refreshes had timeouts; the current snapshot returned results for all four queries. The Java standard library has no documented PLY parser. Ardor3D remains unresolved. ArtiSynth Maspack PlyReader was found through official documentation and parsed the valid control from its 3.9 ZIP, but the distribution includes a noncommercial TetGen component; no separately released BSD-only reader package was established, so it is not counted. See `cell.json`, `registry-snapshot.json`, `leads.json`, `standard.json`, and `verification.json`.

JavaGL Ply 0.0.4 was discovered from its publisher documentation and exact Maven Central artifact; the generic `ply` search omitted it. Its documented `PlyReader.read(InputStream)` returned parsed vertices and face indices from the local control. Maven artifacts, tagged README and MIT license are hash-pinned. deps.dev reports zero known public direct dependents for this exact release, so the rank is tied with the other zero-count packages and does not establish broad adoption. Twelve more qualifying paths are needed for the working target.

Four documentation leads remain unresolved. Ardor3D's documented JogAmp importer is a snapshot continuation absent from the tagged upstream 1.6.0 tree. ArtiSynth Maspack's distribution includes a noncommercial component. JSplat's PLY module is a snapshot and delegates to JavaGL Ply, while pcljava is a snapshot JNI wrapper over PCL with external native dependencies. None is counted without a qualifying pinned release and control run.

F3D 4.0.1's source-built Java binding parsed the valid triangle through its scene API using the same native plugin and VTK PLY reader as the C and C++ bindings. Its source and VTK dependency are hash-pinned. No exact-release deps.dev metric exists for this binding, so it remains unranked; its Homebrew formula count is not combined with Java direct-dependent counts.
