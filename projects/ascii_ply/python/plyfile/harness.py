"""Parse an ASCII PLY mesh from bytes using plyfile."""

from io import BytesIO

from plyfile import PlyData, PlyParseError


def parse_ascii_ply(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    mesh = PlyData.read(BytesIO(data), mmap=False)
    if not mesh.text or "vertex" not in mesh or "face" not in mesh:
        return None
    vertices = mesh["vertex"]
    if not len(vertices):
        return None
    names = vertices.data.dtype.names or ()
    if not all(axis in names for axis in ("x", "y", "z")):
        return None
    first = [float(vertices[0][axis]) for axis in ("x", "y", "z")]
    last = [float(vertices[-1][axis]) for axis in ("x", "y", "z")]
    return {"vertex_count": len(vertices), "face_count": len(mesh["face"]),
            "first_vertex": first, "last_vertex": last}


def fuzz_one_input(data: bytes):
    try:
        parse_ascii_ply(data)
    except PlyParseError:
        pass
