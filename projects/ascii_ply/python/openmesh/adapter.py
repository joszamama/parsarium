"""Read a supplied valid ASCII PLY file through one pinned package API."""

import json
import os
import sys
from pathlib import Path


def summarize(vertices, face_count):
    points = [list(map(float, vertex)) for vertex in vertices]
    return {
        "vertex_count": len(points),
        "face_count": int(face_count),
        "first_vertex": points[0],
        "last_vertex": points[-1],
    }


def parse(name, path):
    if name == "plyfile":
        from plyfile import PlyData
        mesh = PlyData.read(path)
        vertices = [[row[axis] for axis in ("x", "y", "z")] for row in mesh["vertex"]]
        return summarize(vertices, len(mesh["face"]))
    if name == "trimesh":
        import trimesh
        mesh = trimesh.load(path, force="mesh")
        return summarize(mesh.vertices, len(mesh.faces))
    if name == "meshio":
        import meshio
        mesh = meshio.read(path)
        return summarize(mesh.points, len(mesh.cells_dict["triangle"]))
    if name == "pyntcloud":
        from pyntcloud import PyntCloud
        cloud = PyntCloud.from_file(path)
        return summarize(cloud.points[["x", "y", "z"]].to_numpy(), len(cloud.mesh))
    if name == "pyminiply":
        import pyminiply
        vertices, indices, *_ = pyminiply.read(path)
        return summarize(vertices, len(indices))
    if name == "pyvista-miniply":
        import pyvista_miniply
        vertices, indices, *_ = pyvista_miniply.read(path)
        return summarize(vertices, len(indices))
    if name == "polyxios":
        import polyxios
        mesh = polyxios.read(path)
        return summarize(mesh.vertices, len(mesh.element_types))
    if name == "shapeviz":
        import shapeviz
        mesh = shapeviz.load(path)
        return summarize(mesh.vertices, len(mesh.faces))
    if name == "ply-parser":
        from ply_parser import parse_ply_file
        mesh = parse_ply_file(path)
        return summarize(mesh.vertices, len(mesh.faces))
    if name == "py3d":
        import py3d
        mesh = py3d.read_ply(path)
        return summarize(mesh.vertices, len(mesh.faces))
    if name == "pyvista":
        import pyvista
        mesh = pyvista.PLYReader(path).read()
        return summarize(mesh.points, mesh.n_cells)
    if name == "vtk":
        import vtk
        reader = vtk.vtkPLYReader()
        reader.SetFileName(path)
        reader.Update()
        mesh = reader.GetOutput()
        vertices = [mesh.GetPoint(i) for i in range(mesh.GetNumberOfPoints())]
        return summarize(vertices, mesh.GetNumberOfPolys())
    if name == "open3d":
        import open3d
        mesh = open3d.io.read_triangle_mesh(path)
        return summarize(mesh.vertices, len(mesh.triangles))
    if name == "pymeshlab":
        import pymeshlab
        meshes = pymeshlab.MeshSet()
        meshes.load_new_mesh(path)
        mesh = meshes.current_mesh()
        return summarize(mesh.vertex_matrix(), mesh.face_number())
    if name == "point-cloud-utils":
        import point_cloud_utils
        vertices, faces = point_cloud_utils.load_mesh_vf(path)
        return summarize(vertices, len(faces))
    if name == "vedo":
        import vedo
        mesh = vedo.load(path)
        return summarize(mesh.vertices, len(mesh.cells))
    if name == "assimp-py":
        import assimp_py
        import numpy as np
        scene = assimp_py.import_file(path, assimp_py.Process_Triangulate)
        mesh = scene.meshes[0]
        return summarize(np.asarray(mesh.vertices).reshape((-1, 3)), mesh.num_faces)
    if name == "libigl":
        import igl
        vertices, faces = igl.read_triangle_mesh(path)
        return summarize(vertices, len(faces))
    if name == "openmesh":
        import openmesh
        mesh = openmesh.read_trimesh(str(path))
        return summarize(mesh.points(), mesh.n_faces())
    if name == "numpy-stl":
        from stl import mesh as stl_mesh
        mesh = stl_mesh.Mesh.from_ply_file(path)
        return summarize(mesh.vectors.reshape((-1, 3)), len(mesh.vectors))
    if name == "pyassimp":
        if sys.platform == "darwin":
            brew_lib = Path("/opt/homebrew/opt/assimp/lib")
            if brew_lib.is_dir():
                os.environ["LD_LIBRARY_PATH"] = f"{brew_lib}:{os.environ.get('LD_LIBRARY_PATH', '')}"
        import pyassimp
        with pyassimp.load(path) as scene:
            mesh = scene.meshes[0]
            return summarize(mesh.vertices, len(mesh.faces))
    raise ValueError(f"unknown package: {name}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: main.py PACKAGE LOCAL_ASCII_PLY_FILE")
    print(json.dumps(parse(sys.argv[1], sys.argv[2])))
