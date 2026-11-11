"""Build a deterministic one-page PDF 1.4 with a searchable text token."""

from pathlib import Path


ROOT = Path(__file__).resolve().parent
stream = b"BT /F1 18 Tf 72 720 Td (Parsarium) Tj ET\n"
objects = [
    b"<< /Type /Catalog /Pages 2 0 R >>",
    b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
    b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
    b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"endstream",
    b"<< /Title (Parsarium PDF control) /Producer (Parsarium) >>",
]
data = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
offsets = [0]
for index, obj in enumerate(objects, 1):
    offsets.append(len(data))
    data += f"{index} 0 obj\n".encode() + obj + b"\nendobj\n"
xref = len(data)
data += f"xref\n0 {len(offsets)}\n".encode()
data += b"0000000000 65535 f \n"
for offset in offsets[1:]:
    data += f"{offset:010d} 00000 n \n".encode()
data += b"trailer\n<< /Size 7 /Root 1 0 R /Info 6 0 R >>\n"
data += f"startxref\n{xref}\n%%EOF\n".encode()
(ROOT / "one-page.pdf").write_bytes(data)
print(f"Wrote {len(data)} bytes")
