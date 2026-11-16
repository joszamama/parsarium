"""Read one local PLY file through Open3D for AFL++ QEMU feedback."""

import sys
import open3d


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: run-once.py LOCAL_PLY_FILE")
    mesh = open3d.io.read_triangle_mesh(sys.argv[1])
    print(f"vertices={len(mesh.vertices)} faces={len(mesh.triangles)} "
          f"colors={int(mesh.has_vertex_colors())}")


if __name__ == "__main__":
    main()
