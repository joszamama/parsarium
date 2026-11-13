# Java × Matrix Market: verified parser ranking

Three verified third-party Maven package paths; working goal 20, ceiling 30. The metric is deps.dev's exact-release public direct dependent count. It is a partial within-Java adoption proxy and does not measure Matrix Market-specific use. Three Matrix Market string searches returned zero hits; a broad EJML search returned 28 package-name leads. MTJ and SystemDS came from targeted official documentation. Search hits are not parser evidence.

| Rank | Package | Pinned release | Direct dependents | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [mtj](https://github.com/fommil/matrix-toolkits-java/blob/mtj-1.0.4/src/main/java/no/uib/cipr/matrix/io/MatrixVectorReader.java) | com.googlecode.matrix-toolkits-java:mtj:1.0.4 | 18 | 2×3 real coordinate matrix, three entries, value (1,3) = −2 | MTJ native Matrix Market coordinate reader |
| 2 | [ejml-core](https://ejml.org/javadoc/org/ejml/ops/MatrixIO.html) | org.ejml:ejml-core:0.46.1 | 11 | 2×3 real coordinate matrix, three entries, value (1,3) = −2 | EJML native Matrix Market coordinate reader |
| 3 | [systemds](https://systemds.apache.org/docs/3.4.0/api/java/org/apache/sysds/runtime/io/ReaderTextCell.html) | org.apache.systemds:systemds:3.4.0 | 0 | 2×3 real coordinate matrix, three entries, value (1,3) = −2 | Apache SystemDS native Matrix Market text-cell reader |

SystemDS has 1,100 project-wide GitHub stars in the captured snapshot, recorded only as auxiliary adoption evidence. Its exact 3.4.0 release has zero known direct dependents in deps.dev; the metric has coverage and release-age limits. The JDK 21 standard library has no documented Matrix Market parser. The javagl MatrixMarketReader remains an unresolved lead. See `cell.json`, `registry-snapshot.json`, `maven-dependency-lock.json`, `leads.json`, `standard.json`, and `verification.json`.
