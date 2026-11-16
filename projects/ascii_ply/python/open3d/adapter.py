"""Read a local PLY mesh with Open3D's documented triangle-mesh API."""

import json
import sys
from pathlib import Path


def read_mesh(path: Path) -> dict:
    import open3d

    mesh = open3d.io.read_triangle_mesh(str(path))
    vertices = mesh.vertices
    count = len(vertices)
    return {
        "vertex_count": count,
        "face_count": len(mesh.triangles),
        "first_vertex": [float(value) for value in vertices[0]] if count else None,
        "last_vertex": [float(value) for value in vertices[-1]] if count else None,
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: adapter.py LOCAL_PLY_FILE")
    print(json.dumps(read_mesh(Path(sys.argv[1]))))
