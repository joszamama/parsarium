"""Parse an ASCII PLY mesh from bytes using plyfile."""

from io import BytesIO

from plyfile import PlyData, PlyParseError


def parse_ascii_ply(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    mesh = PlyData.read(BytesIO(data), mmap=False)
    if not mesh.text:
        return None
    # Elements and properties the file does not have are reported as 0 or empty.
    face_count = len(mesh["face"]) if "face" in mesh else 0
    if "vertex" not in mesh:
        return {"vertex_count": 0, "face_count": face_count,
                "first_vertex": [], "last_vertex": []}
    vertices = mesh["vertex"]
    names = vertices.data.dtype.names or ()
    axes = [axis for axis in ("x", "y", "z") if axis in names]
    first = [float(vertices[0][axis]) for axis in axes] if len(vertices) else []
    last = [float(vertices[-1][axis]) for axis in axes] if len(vertices) else []
    return {"vertex_count": len(vertices), "face_count": face_count,
            "first_vertex": first, "last_vertex": last}


def fuzz_one_input(data: bytes):
    try:
        parse_ascii_ply(data)
    except PlyParseError:
        pass
