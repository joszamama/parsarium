# PyMeshLab — ASCII PLY / Python

PyMeshLab `2025.7.post1` is pinned in the [manifest](manifest.json). Its Docker control is verified, while native MeshLab parser feedback and source-line coverage are unavailable. See the [control receipt](control-verification.json), [feedback blocker](feedback-blocker.json), and [catalog API evidence](../../../../catalog/ascii_ply/python/pymeshlab/README.md).

From the repository root:

```sh
python3 projects/ascii_ply/python/pymeshlab/control.py verify
python3 projects/ascii_ply/python/pymeshlab/control.py run controls/ascii_ply/triangle.ply
python3 projects/ascii_ply/python/pymeshlab/control.py run YOUR_LOCAL_PLY_FILE
```

`MeshSet.load_new_mesh(local path)` parses the triangle control as three vertices and one face. The valid coloured PLY control loads as three vertices and no faces. The runner builds the pinned image and accepts a local PLY path.

AFL++ QEMU timed out and reported SIGSEGV on the valid control even when instrumentation was limited to MeshLab's `libio_base.so` and the Python executable was excluded. Frida mode parsed the control through a one-shot embedded CPython launcher, but yielded zero tuples when scoped to that PLY plugin, including with dynamic-load range updates disabled. A host-executable-only Frida map is excluded from parser feedback. The [feedback blocker](feedback-blocker.json) records these fixed-control probes. Python binding lines in the control receipt are separate from native PLY parser coverage. This path remains staged and has no verified AFL++ campaign overlay.
