"""Build a deterministic three-page PDF 1.5 with an object stream and xref stream.

Unlike controls/pdf/one-page.pdf (classic xref table, no compressed objects),
the catalog, page tree, pages, and font live in a FlateDecode object stream and
are located through a compressed cross-reference stream. The file is valid PDF
and exercises pdf_oxide's objstm and xref-stream decoding paths.
"""

from pathlib import Path
import zlib


ROOT = Path(__file__).resolve().parent
page = b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 6 0 R >> >> /Contents 7 0 R >>"
packed = {
    1: b"<< /Type /Catalog /Pages 2 0 R >>",
    2: b"<< /Type /Pages /Kids [3 0 R 4 0 R 5 0 R] /Count 3 >>",
    3: page,
    4: page,
    5: page,
    6: b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
}
body = bytearray()
header = bytearray()
for number, obj in packed.items():
    header += f"{number} {len(body)} ".encode()
    body += obj + b"\n"
header = bytes(header).rstrip() + b"\n"
objstm = zlib.compress(header + body, 9)
content = b"BT /F1 18 Tf 72 720 Td (Parsarium) Tj ET\n"

data = bytearray(b"%PDF-1.5\n%\xe2\xe3\xcf\xd3\n")
offsets = {}
offsets[7] = len(data)
data += b"7 0 obj\n<< /Length " + str(len(content)).encode() + b" >>\nstream\n" + content + b"endstream\nendobj\n"
offsets[8] = len(data)
data += (b"8 0 obj\n<< /Type /ObjStm /N " + str(len(packed)).encode()
         + b" /First " + str(len(header)).encode()
         + b" /Filter /FlateDecode /Length " + str(len(objstm)).encode()
         + b" >>\nstream\n" + objstm + b"\nendstream\nendobj\n")
xref_offset = len(data)
offsets[9] = xref_offset
size = 10
rows = bytearray()
for number in range(size):
    if number == 0:
        rows += bytes([0]) + (0).to_bytes(4, "big") + (65535).to_bytes(2, "big")
    elif number in packed:
        rows += bytes([2]) + (8).to_bytes(4, "big") + (number - 1).to_bytes(2, "big")
    else:
        rows += bytes([1]) + offsets[number].to_bytes(4, "big") + (0).to_bytes(2, "big")
xref = zlib.compress(bytes(rows), 9)
data += (b"9 0 obj\n<< /Type /XRef /Size " + str(size).encode()
         + b" /W [1 4 2] /Root 1 0 R /Filter /FlateDecode /Length "
         + str(len(xref)).encode() + b" >>\nstream\n" + xref + b"\nendstream\nendobj\n")
data += f"startxref\n{xref_offset}\n%%EOF\n".encode()
(ROOT / "valid-objstm.pdf").write_bytes(data)
print(f"Wrote {len(data)} bytes")
