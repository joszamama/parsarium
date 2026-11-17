# McCode — ASCII PLY / C

McCode 3.10.2's tagged [`interoff-lib` API](https://github.com/mccode-dev/McCode/blob/v3.10.2/common/lib/share/interoff-lib.h) documents `off_init(localPath, ..., off_struct*)`. The [Guide_anyshape component](https://github.com/mccode-dev/McCode/blob/v3.10.2/mcstas-comps/optics/Guide_anyshape.comp) uses that reader for local geometry. This harness passes local polygonal ASCII PLY bytes through the same `off_init` parser and reports the mesh's vertex count, face count, length, and width. McCode 3.10.2 [rejects zero-face PLY point clouds](https://github.com/mccode-dev/McCode/blob/v3.10.2/common/lib/share/interoff-lib.c#L387-L391), so this path covers meshes with at least one face.

The Docker build hash-checks the tagged C source and header. McStas normally expands one `%include` directive and supplies generic generated-instrument helpers. The build removes that directive from a copy of the header and supplies local-file I/O, geometry primitives, and unused display stubs. The compiled `interoff-lib.c` is byte-identical to the pinned upstream source. This target runs one file per process because the upstream parser can call `exit` on rejected input. Native in-process campaign preparation is marked unsupported; the AFL++ file target remains available.

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply c mccode
python3 parsarium.py run ascii_ply c mccode controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply c mccode CORPUS_DIR runs/ply-mccode-replay
python3 parsarium.py afl build ascii_ply c mccode
python3 parsarium.py afl prepare ascii_ply c mccode runs/ply-mccode-afl
```

Replace `CORPUS_DIR` with a directory of PLY files. AFL++ preparation creates a one-file-per-process target and seed without starting a campaign. See the [manifest](manifest.json), [control receipt](verification.json), and [catalog record](../../../../catalog/ascii_ply/c/mccode/README.md).

The fixed triangle control covers 240 lines in `interoff-lib.c`, including its PLY header branch, vertex reader, and face-index reader. The [AFL++ receipt](../../../../fuzzing/afl-native/ascii_ply/c/mccode/verification.json) records 87 edges. A separate [fixed-input feedback check](../../../../fuzzing/afl-native/ascii_ply/c/mccode/feedback-validation.json) confirms an identical map on repeat and a different map for a valid four-vertex PLY. These checks run no mutation campaign.
