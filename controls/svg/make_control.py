"""Generate a small SVG 1.1 image with two distinct shapes."""

from pathlib import Path

control = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="2" height="1" viewBox="0 0 2 1">'
    '<rect x="0" y="0" width="1" height="1" fill="#ff0000"/>'
    '<rect x="1" y="0" width="1" height="1" fill="#00ff00"/>'
    '</svg>\n'
).encode("utf-8")
out = Path(__file__).resolve().parent / "red-green.svg"
out.write_bytes(control)
print(f"Wrote {len(control)} SVG bytes")

path_control = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="4" height="2" viewBox="0 0 4 2">'
    '<rect x="0" y="0" width="2" height="2" fill="#ff0000"/>'
    '<path d="M 2 0 L 4 0 L 4 2 Z" fill="#0000ff"/>'
    '</svg>\n'
).encode("utf-8")
path_out = Path(__file__).resolve().parent / "red-blue-path.svg"
path_out.write_bytes(path_control)
print(f"Wrote {len(path_control)} SVG path-control bytes")
