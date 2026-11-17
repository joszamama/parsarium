# lwjgl-assimp — ASCII PLY / Java

Pinned release: `org.lwjgl:lwjgl-assimp:3.4.3`. The adapter calls `Assimp.aiImportFile(path, 0)` and reads the resulting `aiScene`. The control is a valid triangle with 3 vertices, 1 face and indices `[0,1,2]`.

The [manifest](manifest.json), [source lock](source-lock.json) and [Docker receipt](verification.json) identify the published Java and native artifacts. The control runs against both LWJGL's unmodified `libassimp.so` and a coverage build of the matching [LWJGL-CI/assimp revision](https://github.com/LWJGL-CI/assimp/commit/34f99dd81d93f2759d57c6c4dbfc85aa40a4b3d9). The build checks native symbols, SONAME, dependencies and the struct layout read by LWJGL. Both libraries return the same parsed scene.

```sh
python3 parsarium.py build ascii_ply java lwjgl_assimp
python3 parsarium.py run ascii_ply java lwjgl_assimp controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply java lwjgl_assimp CORPUS_DIR runs/lwjgl-ply-replay
python3 parsarium.py afl build ascii_ply java lwjgl_assimp
python3 parsarium.py afl prepare ascii_ply java lwjgl_assimp runs/lwjgl-ply-afl
python3 parsarium.py afl run runs/lwjgl-ply-afl --check
```

The [AFL++ overlay](../../../../fuzzing/afl-native/ascii_ply/java/lwjgl_assimp) launches the Java harness with the instrumented native library. It converts executed Assimp `AssetLib/Ply` source regions and branches into AFL++ feedback; Java wrapper lines are excluded. Its [receipt](../../../../fuzzing/afl-native/ascii_ply/java/lwjgl_assimp/verification.json) records a second valid PLY control with different native coverage. The Jazzer entry remains available, but its JVM instrumentation does not observe native Assimp parser coverage.

The native library is a clang coverage rebuild of the pinned revision, while the published library is stripped and built with GCC. A native crash can terminate the JVM before its LLVM profile is written; AFL++ still observes a crashing run. The native build does not include ASan or UBSan.
