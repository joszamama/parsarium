"""Capture bounded PyPI ASCII PLY leads and comparable adoption metrics."""

import json
from pathlib import Path
from snapshot_pypi_png import INDEX_URL, main, read_json

ROOT = Path(__file__).resolve().parents[1]
TERMS = ("ply", "mesh", "pointcloud", "point-cloud", "trimesh", "open3d",
         "vtk", "assimp", "pyvista", "geometry", "pcd")

if __name__ == "__main__":
    cell = ROOT / "data" / "python" / "ascii_ply"
    main(cell, TERMS)
    snapshot_path = cell / "registry-snapshot.json"
    snapshot = json.loads(snapshot_path.read_text())
    index = read_json(INDEX_URL, "application/vnd.pypi.simple.v1+json")
    names = sorted((item["name"] for item in index["projects"]
                    if item["name"].lower().startswith("ply")), key=str.casefold)
    snapshot["search"].append({
        "query": "project name starts with 'ply'", "url": INDEX_URL,
        "total": len(names), "limit": 100,
        "ordering": "case-insensitive project-name order; not a popularity order",
        "hits": [{"rank": i, "name": name} for i, name in enumerate(names[:100], 1)],
    })
    snapshot_path.write_text(json.dumps(snapshot, indent=2) + "\n")
    print(f"ASCII PLY snapshot: {sum(len(row['hits']) for row in snapshot['search'])} hits across {len(snapshot['search'])} searches")
