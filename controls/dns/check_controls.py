"""Check the DNS controls with a small hand-written RFC 1035 decoder.

This is the oracle for the expected summaries. It uses no DNS library: the
header is unpacked with struct, names are read label by label and follow
compression pointers (only backwards, at most 64 jumps), and the decoder
requires every byte of the message to be consumed. RDATA is decoded for A,
NS, CNAME, PTR, MX, TXT and AAAA. IPv6 text uses the standard library's
ipaddress module (RFC 5952 form).

Summary fields, shared by every harness:
  id, qr, opcode, aa, tc, rd, ra, z, rcode, qdcount, ancount, nscount, arcount
  questions: [{name, type, class}]
  answers / authority / additional: [{name, type, class, ttl, rdata}]
Names are lowercase, absolute, with a trailing dot. Types and classes are
numbers. RDATA text: A dotted quad; AAAA RFC 5952; CNAME/NS/PTR a name;
MX "<preference> <exchange>"; TXT the quoted strings joined by spaces.
"""

from hashlib import sha256
import ipaddress
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parent
EXPECTED = ROOT / "expected.json"


def read_name(data: bytes, offset: int) -> tuple[str, int]:
    labels, end, jumps, position = [], None, 0, offset
    while True:
        length = data[position]
        if length & 0xC0 == 0xC0:
            target = ((length & 0x3F) << 8) | data[position + 1]
            if target >= position or jumps >= 64:
                raise ValueError("compression pointer must point backwards")
            if end is None:
                end = position + 2
            position, jumps = target, jumps + 1
            continue
        if length & 0xC0:
            raise ValueError("reserved label type")
        position += 1
        if length == 0:
            break
        labels.append(data[position:position + length].decode("ascii").lower())
        position += length
    return ".".join(labels) + ".", end if end is not None else position


def rdata_text(data: bytes, rtype: int, start: int, length: int) -> str:
    raw = data[start:start + length]
    if rtype == 1 and length == 4:
        return ".".join(str(octet) for octet in raw)
    if rtype == 28 and length == 16:
        return str(ipaddress.IPv6Address(raw))
    if rtype in (2, 5, 12):
        target, end = read_name(data, start)
        if end != start + length:
            raise ValueError("name RDATA length mismatch")
        return target
    if rtype == 15:
        exchange, end = read_name(data, start + 2)
        if end != start + length:
            raise ValueError("MX RDATA length mismatch")
        return f"{struct.unpack('>H', raw[:2])[0]} {exchange}"
    if rtype == 16:
        strings, position = [], 0
        while position < length:
            size = raw[position]
            strings.append('"' + raw[position + 1:position + 1 + size].decode("ascii") + '"')
            position += 1 + size
        if position != length:
            raise ValueError("TXT RDATA length mismatch")
        return " ".join(strings)
    raise ValueError(f"RDATA type {rtype} is outside the control subset")


def summarize(data: bytes) -> dict:
    ident, flags, qd, an, ns, ar = struct.unpack(">HHHHHH", data[:12])
    summary = {"id": ident, "qr": flags >> 15, "opcode": (flags >> 11) & 0xF,
               "aa": (flags >> 10) & 1, "tc": (flags >> 9) & 1, "rd": (flags >> 8) & 1,
               "ra": (flags >> 7) & 1, "z": (flags >> 4) & 7, "rcode": flags & 0xF,
               "qdcount": qd, "ancount": an, "nscount": ns, "arcount": ar,
               "questions": [], "answers": [], "authority": [], "additional": []}
    offset = 12
    for _ in range(qd):
        owner, offset = read_name(data, offset)
        qtype, qclass = struct.unpack(">HH", data[offset:offset + 4])
        offset += 4
        summary["questions"].append({"name": owner, "type": qtype, "class": qclass})
    for section, count in (("answers", an), ("authority", ns), ("additional", ar)):
        for _ in range(count):
            owner, offset = read_name(data, offset)
            rtype, rclass, ttl, length = struct.unpack(">HHIH", data[offset:offset + 10])
            offset += 10
            if offset + length > len(data):
                raise ValueError("RDATA runs past the message")
            summary[section].append({"name": owner, "type": rtype, "class": rclass, "ttl": ttl,
                                     "rdata": rdata_text(data, rtype, offset, length)})
            offset += length
    if offset != len(data):
        raise ValueError("trailing bytes after the last record")
    return summary


def main() -> None:
    expected = json.loads(EXPECTED.read_text())
    for name, record in expected.items():
        data = (ROOT / name).read_bytes()
        if sha256(data).hexdigest() != record["sha256"] or len(data) != record["bytes"]:
            raise SystemExit(f"{name}: control bytes changed")
        observed = summarize(data)
        if observed != record["summary"]:
            raise SystemExit(f"{name}: summary differs:\n{json.dumps(observed, indent=2)}")
        print(f"{name}: {len(data)} bytes, sha256 {record['sha256']}, summary matches")


if __name__ == "__main__":
    main()
