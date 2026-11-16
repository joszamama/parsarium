# f3d — ASCII PLY / C++

Pinned release: `4.0.1`, built against VTK `9.7.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/cpp/f3d/README.md)

The pinned Docker control parsed one triangle as one file, one actor, three points, and one cell. LLVM coverage reached 329 F3D source lines, including its PLY reader, and 573 underlying VTK PLY source lines. The AFL++ overlay produced 10,839 feedback edges on the same valid control.

The harness writes each input to a local `.ply` path, loads it with `f3d::scene::add` on an `engine::createNone()` engine, and prints `getSceneInfo` as files, actors, points, and cells. F3D's static native plugin selects its `PLYReader` entry, which runs `vtkF3DPLYReader` over VTK's `vtkPLYReader` and `vtkPLY`. This project shares the VTK parser family with [vtk](../vtk/README.md) and does not count as a separate family.

The control check requires covered lines in F3D's generated `reader_PLYReader.h`, `vtkF3DPLYReader.cxx`, and VTK's `vtkPLYReader.cxx` and `vtkPLY.cxx`. Coverage and sanitizers are limited to the F3D native plugin targets and the two VTK PLY objects. The AFL++ overlay rebuilds VTK and F3D with AFL++'s compiler, so feedback edges also include the rest of VTK and libf3d.

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply cpp f3d
python3 parsarium.py run ascii_ply cpp f3d controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply cpp f3d CORPUS_DIR runs/ascii_ply-f3d-replay
python3 parsarium.py afl build ascii_ply cpp f3d
python3 parsarium.py afl prepare ascii_ply cpp f3d runs/ascii_ply-f3d-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
