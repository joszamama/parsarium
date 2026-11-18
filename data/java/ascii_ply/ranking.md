# JAVA × ASCII PLY: selected parsers

7 control-verified third-party paths selected from 21 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

deps.dev version-level directDependentCount.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [lwjgl-assimp](https://javadoc.lwjgl.org/org/lwjgl/assimp/Assimp.html) | 3.4.3 | 13 | ASCII PLY triangle vertex and face counts, parsed face indices | LWJGL Java binding over native Assimp PLY importer; same Assimp parser family as C++ path |
| 2 | [boofcv-io](https://boofcv.org/index.php?title=Example_Load_and_Save_Point_Clouds) | 1.6.0 | 11 | ASCII triangle, three vertices, one face, parsed indices [0,1,2] | BoofCV native Java PLY mesh reader |
| 3 | [scalismo_3](https://github.com/unibas-gravis/scalismo/blob/v1.0-RC1/src/main/scala/scalismo/io/MeshIO.scala) | 1.0-RC1 | 2 | ASCII PLY triangle vertices, face list and parsed point ids | Scalismo pure Scala PLY reader (scalismo.io.ply) |

## Supplemental numeric evidence

These paths lack a positive primary metric. Their figures are reported separately and are not compared numerically with the table above.

| Supplemental rank | Package | Release | Signal | Value | Parsed scope | Parser family |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | [f3d](https://github.com/f3d-app/f3d/blob/v4.0.1/java/Scene.java) | 4.0.1 | [GitHub upstream stars](https://github.com/f3d-app/f3d) | 5,074 | ASCII triangle produced three parsed points and one cell | F3D native PLY plugin over VTK vtkPLYReader |
| 2 | [sceneview-core](https://github.com/sceneview/sceneview/blob/v4.69.5/sceneview-core/src/commonMain/kotlin/io/github/sceneview/core/ply/PlyLoader.kt) | 4.69.5 | [GitHub upstream stars](https://github.com/sceneview/sceneview) | 1,377 | ASCII PLY triangle vertices, triangulated face and parsed indices | SceneView Core pure Kotlin PLY parser |
| 3 | [jzy3d-core](https://doc.jzy3d.org/javadoc/2.2.1/org/jzy3d/io/ply/Ply.html) | 2.2.1 | [GitHub upstream stars](https://github.com/jzy3d/jzy3d-api) | 310 | ASCII triangle vertex positions (three vertices, second X and third Y); faces not exposed by this API | Jzy3d public PLY vertex API over jPLY |
| 4 | [kotlin-assimp](https://github.com/kotlin-graphics/assimp/tree/v4.0#code) | v4.0 | [GitHub upstream stars](https://github.com/kotlin-graphics/assimp) | 105 | ASCII PLY triangle, three vertices, one face, parsed indices [0,1,2] | Kotlin-graphics JVM Assimp port PLY importer |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
