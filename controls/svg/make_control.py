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
