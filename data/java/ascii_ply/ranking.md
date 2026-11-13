# Java × ASCII PLY: verified parser ranking

Seven verified third-party Maven package paths; working goal 20, ceiling 30. The metric is deps.dev's known public direct dependents for each exact release, a limited within-Java adoption proxy. It does not measure PLY-specific use, and zero can reflect coverage or version-age gaps. LWJGL Assimp and MonkeyWrench share the native Assimp PLY parser family with the C++ Assimp path.

| Rank | Package | Pinned release | Direct dependents | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [LWJGL Assimp](https://javadoc.lwjgl.org/org/lwjgl/assimp/Assimp.html) | org.lwjgl:lwjgl-assimp:3.4.3 | 13 | ASCII triangle vertices, face and indices | LWJGL binding over native Assimp PLY importer |
| 2 | [jPLY](https://github.com/smurn/jPLY) | org.smurn:jply:0.2.0 | 0 | ASCII triangle vertices, face and indices | jPLY native PLY element reader |
| 2 | [MeshIO](https://github.com/NathanJAdams/MeshIO#using-formats-directly) | com.ripplargames:meshio:2.1.2 | 0 | ASCII triangle vertices, face and indices | MeshIO native ASCII PLY mesh reader |
| 2 | [mesh-ply](https://github.com/kazocsaba/mesh-ply/blob/mesh-ply-1.1.0/src/main/java/hu/kazocsaba/v3d/mesh/format/ply/PlyReader.java) | hu.kazocsaba.geom3d:mesh-ply:1.1.0 | 0 | ASCII triangle vertices, face and indices | kazocsaba mesh-ply native PLY reader |
| 2 | [pcutil](https://github.com/zhoujianling/PointCloudUtilities#plyreader) | cn.jimmiez:pcutil:0.3.0 | 0 | ASCII triangle vertices, face and indices | PointCloudUtilities annotated PLY reader |
| 2 | [MonkeyWrench](https://github.com/stephengold/MonkeyWrench#how-to-add-monkeywrench-to-an-existing-project) | com.github.stephengold:MonkeyWrench:1.0.1 | 0 | ASCII triangle vertices, face and indices | JMonkeyEngine wrapper over LWJGL Assimp PLY importer |
| 2 | [JavaGL Ply](https://github.com/javagl/Ply/tree/ply-parent-0.0.4) | de.javagl:ply:0.0.4 | 0 | ASCII triangle vertices, face and indices | JavaGL native Java PLY reader |

Four bounded Maven search queries saved seven name hits; prior refreshes had timeouts; the current snapshot returned results for all four queries. The Java standard library has no documented PLY parser. Ardor3D remains unresolved. ArtiSynth Maspack PlyReader was found through official documentation and parsed the valid control from its 3.9 ZIP, but the distribution includes a noncommercial TetGen component; no separately released BSD-only reader package was established, so it is not counted. See `cell.json`, `registry-snapshot.json`, `leads.json`, `standard.json`, and `verification.json`.

JavaGL Ply 0.0.4 was discovered from its publisher documentation and exact Maven Central artifact; the generic `ply` search omitted it. Its documented `PlyReader.read(InputStream)` returned parsed vertices and face indices from the local control. Maven artifacts, tagged README and MIT license are hash-pinned. deps.dev reports zero known public direct dependents for this exact release, so the rank is tied with the other zero-count packages and does not establish broad adoption. Thirteen more qualifying paths are needed for the working target.
