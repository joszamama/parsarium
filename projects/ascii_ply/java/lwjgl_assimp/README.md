# lwjgl-assimp — ASCII PLY / Java

Pinned release: `3.4.3`. [Manifest](manifest.json) · [source lock](source-lock.json) · [control receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/java/lwjgl-assimp/README.md)

`Assimp.aiImportFile(path, 0)` from `org.lwjgl:lwjgl-assimp:3.4.3` hands the path to native Assimp through LWJGL's `dlsym`-resolved function pointers. The PLY parser is Assimp's C++ `PlyLoader`/`PlyParser`; the Java classes only marshal the path and read `aiScene`/`aiMesh`/`aiFace` fields by offset.

## Native artifact and source route

| Item | Pin |
| --- | --- |
| `lwjgl-assimp-3.4.3-natives-linux-arm64.jar` | sha256 `61abb8b3…4b7dfa`, matches Central sha1 `353122639d…` |
| bundled `libassimp.so` | sha256 `481ea9e2…f6ace4`, SONAME `libassimp.so.6`, NEEDED `libdraco.so.9`, GCC 12.3.0, stripped |
| revision named in the jar | `META-INF/.../libassimp.so.git` = upstream assimp `392a658f` |
| rebuilt source | [LWJGL-CI/assimp `34f99dd`](https://github.com/LWJGL-CI/assimp/commit/34f99dd81d93f2759d57c6c4dbfc85aa40a4b3d9) = `392a658f` + LWJGL zlib update + LWJGL CI config, archive sha256 `1b662c12…fbb683` |

All Maven hashes in [source-lock.json](source-lock.json) were checked against Central's `.sha1` files on 2026-11-17. LWJGL-CI's `lwjgl.yml` records `HEAD~2` of the built commit in `libassimp.so.git`; the fork's only branch, `master`, is at `34f99dd` (2026-07-08), whose `HEAD~2` is `392a658f`. The CI commit changes only CMake minimum versions, warning flags and one GCC pragma.

`build-native.sh` rebuilds `libassimp.so` and `libdraco.so` from that tree with the LWJGL CI CMake options (`Release`, `ASSIMP_BUILD_DRACO=ON`, `ASSIMP_BUILD_ZLIB=ON`, `_FORTIFY_SOURCE=0`), using clang 18 with `-O1 -fprofile-instr-generate -fcoverage-mapping` instead of GCC 12. The build stops unless:

- SONAME and the `libdraco` dependency match the stock pair;
- the rebuilt library exports every `ai*` symbol the stock library exports;
- `offsetof`/`sizeof` for the `aiScene`, `aiMesh` and `aiFace` fields the adapter reads, compiled from the same headers, equal the layout LWJGL 3.4.3 computes in Java (`AbiLayout.java` versus `abi_layout.c`).

The LWJGL Java classes and `liblwjgl.so` are not rebuilt. The rebuilt native is a coverage build of the same revision and options, not the published binary; compiler and optimisation level differ.

## Control receipt

`run-control.sh` runs the control twice with the same Java classes:

1. over the unmodified natives-linux-arm64 `libassimp.so`/`libdraco.so` (`/work/native-stock`); the output must be `{"vertices":3,"faces":1,"indices":[0,1,2]}`;
2. over the instrumented rebuild (`/work/native`) with JaCoCo attached; the output must match again.

The adapter sets absolute `org.lwjgl.assimp.libname`/`draco.libname` paths and checks the loaded path through `Assimp.getLibrary().getPath()`, so neither run can fall back to another copy.

Coverage is reported in two groups that are never merged:

| Group | Manifest field | Source | Tool |
| --- | --- | --- | --- |
| Java wrapper | `coverage_subject_prefix` `/work/parser-source/` | `lwjgl-assimp-3.4.3-sources.jar` | JaCoCo 0.8.14 |
| Native PLY parser | `underlying_coverage_subject_prefix` `/work/source/code/AssetLib/Ply/` | LWJGL-CI/assimp `34f99dd` | LLVM 18 `llvm-cov export` |

Only the second group is parser coverage. The wrapper group shows which binding code ran.

## Fuzz engine

`GenericHarness.fuzzerTestOneInput` is the Jazzer entry. Jazzer instruments JVM bytecode only. The native library carries LLVM profile counters, not SanitizerCoverage, so a Jazzer campaign receives wrapper feedback and no native parser feedback. The native library is also built without sanitizers. Native AFL++ feedback is planned in [AFL_PLAN.md](AFL_PLAN.md).

## Run from the repository root

The pinned control has been verified in Docker:

```sh
python3 parsarium.py build ascii_ply java lwjgl_assimp
python3 parsarium.py run ascii_ply java lwjgl_assimp controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply java lwjgl_assimp CORPUS_DIR runs/ascii_ply-lwjgl_assimp-replay
```

The AFL++ commands need the overlay described in [AFL_PLAN.md](AFL_PLAN.md). The generic Java bridge alone would produce wrapper-only feedback.

## Status

The Docker control passes with both stock and source-built native libraries. Coverage reaches 420 Java wrapper lines and 563 native Assimp PLY importer lines. AFL++ native parser feedback remains pending. Open limits:

- the exact CI run that produced the published `.so` is inferred from `libassimp.so.git` and the branch head, not from a build log;
- the profile runtime writes at JVM exit through `atexit`; a native crash leaves no profile for that run.
