"""dnslib decoder over local DNS message bytes through dnslib.DNSRecord.parse(packet)."""

import dnslib

SUBSET = {1, 2, 5, 12, 15, 16, 28}  # A, NS, CNAME, PTR, MX, TXT, AAAA


def absolute(label) -> str:
    text = str(label).lower()
    return text if text.endswith(".") else text + "."


def rdata(record) -> str:
    if record.rtype not in SUBSET:
        raise ValueError(f"record type {record.rtype} is outside the control subset")
    # dnslib's own presentation text: dotted quad, compressed IPv6, names with a trailing dot,
    # "<preference> <exchange>" for MX and quoted strings for TXT.
    text = record.rdata.toZone()
    if record.rtype in (2, 5, 12):
        return absolute(text)
    if record.rtype == 15:
        preference, exchange = text.split(" ", 1)
        return f"{preference} {absolute(exchange)}"
    return text


def records(section) -> list:
    return [{"name": absolute(record.rname), "type": record.rtype, "class": record.rclass,
             "ttl": record.ttl, "rdata": rdata(record)} for record in section]


def parse_dns(data: bytes) -> dict:
    if not data or len(data) > 65535:
        raise ValueError("input outside harness limit")
    message = dnslib.DNSRecord.parse(data)
    header = message.header
    questions = [{"name": absolute(item.qname), "type": item.qtype, "class": item.qclass}
                 for item in message.questions]
    # dnslib exposes the reserved Z bit, AD and CD as separate header properties.
    return {"id": header.id, "qr": header.qr, "opcode": header.opcode, "aa": header.aa,
            "tc": header.tc, "rd": header.rd, "ra": header.ra,
            "z": (header.z << 2) | (header.ad << 1) | header.cd, "rcode": header.rcode,
            "qdcount": header.q, "ancount": header.a, "nscount": header.auth, "arcount": header.ar,
            "questions": questions, "answers": records(message.rr), "authority": records(message.auth),
            "additional": records(message.ar)}


def fuzz_one_input(data: bytes):
    try:
        parse_dns(data)
    except Exception:  # dnslib raises DNSError, BufferError and DNSLabelError on malformed input
        pass
