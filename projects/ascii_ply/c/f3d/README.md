# f3d — ASCII PLY / C

Pinned release: `4.0.1`, built against VTK `9.7.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/c/f3d/README.md)

The pinned Docker control parsed one triangle as one file, one actor, three points, and one cell. LLVM coverage reached 397 F3D source lines, including the C binding and PLY plugin, plus 573 underlying VTK PLY lines. The AFL++ overlay produced 10,908 feedback edges.

The C harness writes each input to a local `.ply` path, creates an engine with `f3d_engine_create_none`, loads the file with `f3d_scene_add`, and prints `f3d_scene_get_scene_info` as files, actors, points, and cells. The build enables F3D's C binding (`F3D_BINDINGS_C`), which wraps the same `f3d::scene` that the [C++ project](../../cpp/f3d/README.md) calls. F3D's static native plugin selects its `PLYReader` entry, which runs `vtkF3DPLYReader` over VTK's `vtkPLYReader` and `vtkPLY`. This project shares the VTK parser family with the C++ F3D and VTK projects and does not count as a separate family.

The control check requires covered lines in F3D's `scene_c_api.cxx`, generated `reader_PLYReader.h`, `vtkF3DPLYReader.cxx`, and VTK's `vtkPLYReader.cxx` and `vtkPLY.cxx`. Coverage and sanitizers are limited to the C binding, the native plugin targets, and the two VTK PLY objects. The AFL++ overlay rebuilds VTK and F3D with AFL++'s compiler, so feedback edges also include the rest of VTK and libf3d.

The runtime image sets `HOME` and `XDG_CACHE_HOME` to `/tmp`, so F3D can write its cache on the tmpfs of a read-only container.

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply c f3d
python3 parsarium.py run ascii_ply c f3d controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply c f3d CORPUS_DIR runs/ascii_ply-f3d-c-replay
python3 parsarium.py afl build ascii_ply c f3d
python3 parsarium.py afl prepare ascii_ply c f3d runs/ascii_ply-f3d-c-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
