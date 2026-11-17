"""dpkt DNS decoder over local DNS message bytes through dpkt.dns.DNS(buf)."""

import socket

import dpkt


def absolute(name: str) -> str:
    text = name.lower()
    return text if text.endswith(".") else text + "."


def rdata(record) -> str:
    # socket.inet_ntop only formats the address bytes dpkt decoded; it opens no socket.
    if record.type == dpkt.dns.DNS_A:
        return socket.inet_ntop(socket.AF_INET, record.ip)
    if record.type == dpkt.dns.DNS_AAAA:
        return socket.inet_ntop(socket.AF_INET6, record.ip6)
    if record.type == dpkt.dns.DNS_CNAME:
        return absolute(record.cname)
    if record.type == dpkt.dns.DNS_NS:
        return absolute(record.nsname)
    if record.type == dpkt.dns.DNS_PTR:
        return absolute(record.ptrname)
    if record.type == dpkt.dns.DNS_MX:
        preference = record.preference
        # dpkt 1.9.8 stores the MX preference as the 1-tuple returned by struct.unpack.
        if isinstance(preference, tuple):
            preference = preference[0]
        return f"{preference} {absolute(record.mxname)}"
    if record.type == dpkt.dns.DNS_TXT:
        return " ".join('"' + (item.decode("latin-1") if isinstance(item, bytes) else item) + '"'
                        for item in record.text)
    raise ValueError(f"record type {record.type} is outside the control subset")


def records(section) -> list:
    return [{"name": absolute(record.name), "type": record.type, "class": record.cls,
             "ttl": record.ttl, "rdata": rdata(record)} for record in section]


def parse_dns(data: bytes) -> dict:
    if not data or len(data) > 65535:
        raise ValueError("input outside harness limit")
    message = dpkt.dns.DNS(data)
    questions = [{"name": absolute(item.name), "type": item.type, "class": item.cls} for item in message.qd]
    answers, authority, additional = records(message.an), records(message.ns), records(message.ar)
    # message.op is the 16-bit flags word dpkt unpacked; z takes its Z, AD and CD bits.
    return {"id": message.id, "qr": message.qr, "opcode": message.opcode, "aa": message.aa,
            "tc": message.tc, "rd": message.rd, "ra": message.ra, "z": (message.op >> 4) & 7,
            "rcode": message.rcode, "qdcount": len(questions), "ancount": len(answers),
            "nscount": len(authority), "arcount": len(additional), "questions": questions,
            "answers": answers, "authority": authority, "additional": additional}


def fuzz_one_input(data: bytes):
    try:
        parse_dns(data)
    except Exception:  # dpkt raises NeedData, UnpackError, struct.error and IndexError on malformed input
        pass
