# vtk — ASCII PLY / C++

Pinned release: `9.7.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/cpp/vtk/README.md)

The harness writes each input to a temporary local `.ply` file and reads it with `vtkPLYReader::SetFileName`, `Update`, and `GetOutput`. The build compiles the minimal static VTK module closure of `VTK::IOPLY`, then recompiles `IO/PLY/vtkPLYReader.cxx` and the bundled `IO/PLY/vtkPLY.cxx` parser with coverage and sanitizer instrumentation.

The valid control passed with 564 covered VTK PLY source lines and 3,014 AFL++ feedback edges.

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply cpp vtk
python3 parsarium.py run ascii_ply cpp vtk controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply cpp vtk CORPUS_DIR runs/ascii_ply-vtk-replay
python3 parsarium.py afl build ascii_ply cpp vtk
python3 parsarium.py afl prepare ascii_ply cpp vtk runs/ascii_ply-vtk-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
