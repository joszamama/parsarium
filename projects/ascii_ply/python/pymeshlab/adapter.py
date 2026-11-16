"""Read a local ASCII PLY mesh through PyMeshLab's MeshSet API."""

import json
import sys
from pathlib import Path


def read_mesh(path: Path) -> dict:
    import pymeshlab

    meshes = pymeshlab.MeshSet()
    meshes.load_new_mesh(str(path))
    mesh = meshes.current_mesh()
    vertices = mesh.vertex_matrix()
    count = mesh.vertex_number()
    return {
        "vertex_count": count,
        "face_count": mesh.face_number(),
        "first_vertex": [float(value) for value in vertices[0]] if count else None,
        "last_vertex": [float(value) for value in vertices[-1]] if count else None,
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: adapter.py LOCAL_PLY_FILE")
    print(json.dumps(read_mesh(Path(sys.argv[1]))))
