"""Write the two valid DNS message controls byte for byte (RFC 1035 section 4).

No DNS library is used. Names are written as length-prefixed labels, and the
response uses explicit compression pointers (RFC 1035 section 4.1.4) to the
question name at offset 12 and to its "example.test" suffix at offset 16.
"""

from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parent
TYPE_A, TYPE_CNAME, TYPE_MX, TYPE_AAAA = 1, 5, 15, 28
CLASS_IN = 1


def name(*labels: str) -> bytes:
    return b"".join(bytes([len(label)]) + label.encode("ascii") for label in labels) + b"\x00"


def pointer(offset: int) -> bytes:
    return struct.pack(">H", 0xC000 | offset)


def header(ident: int, flags: int, qd: int, an: int, ns: int, ar: int) -> bytes:
    return struct.pack(">HHHHHH", ident, flags, qd, an, ns, ar)


def rr(owner: bytes, rtype: int, ttl: int, rdata: bytes) -> bytes:
    return owner + struct.pack(">HHIH", rtype, CLASS_IN, ttl, len(rdata)) + rdata


def query() -> bytes:
    # id 0x1234, standard query, RD set; one question: example.test. A IN
    return header(0x1234, 0x0100, 1, 0, 0, 0) + name("example", "test") + struct.pack(">HH", TYPE_A, CLASS_IN)


def response() -> bytes:
    # id 0xabcd, QR RD RA, NOERROR; question www.example.test. A IN at offset 12.
    message = header(0xABCD, 0x8180, 1, 4, 0, 0)
    assert len(message) == 12
    message += name("www", "example", "test") + struct.pack(">HH", TYPE_A, CLASS_IN)
    question_name, suffix = 12, 16  # "\x03www" is 4 bytes, so "\x07example" starts at 16
    assert message[suffix:suffix + 8] == b"\x07example"
    message += rr(pointer(question_name), TYPE_CNAME, 3600, pointer(suffix))
    message += rr(pointer(suffix), TYPE_A, 300, bytes([192, 0, 2, 10]))
    message += rr(pointer(suffix), TYPE_AAAA, 600, bytes.fromhex("20010db8000000000000000000000010"))
    message += rr(pointer(suffix), TYPE_MX, 7200, struct.pack(">H", 10) + b"\x04mail" + pointer(suffix))
    return message


if __name__ == "__main__":
    for filename, data in (("query.bin", query()), ("response.bin", response())):
        (ROOT / filename).write_bytes(data)
        print(f"Wrote {filename}: {len(data)} bytes")
