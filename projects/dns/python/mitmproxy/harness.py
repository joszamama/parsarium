"""mitmproxy DNS decoder over local DNS message bytes through mitmproxy.dns.DNSMessage.unpack."""

import struct

from mitmproxy import dns
from mitmproxy.net.dns import domain_names, types


def absolute(name: str) -> str:
    text = name.lower()
    return text if text.endswith(".") else text + "."


def rdata(record) -> str:
    # unpack() has already decompressed names inside CNAME/NS/PTR/MX RDATA. A/AAAA text is str() of the
    # ipaddress objects behind the record's ipv4_address/ipv6_address properties; CNAME/NS/PTR use its
    # domain_name property; the MX exchange is read with the library's domain_names.unpack_from.
    if record.type == types.A:
        return str(record.ipv4_address)
    if record.type == types.AAAA:
        return str(record.ipv6_address)
    if record.type in (types.CNAME, types.NS, types.PTR):
        return absolute(record.domain_name)
    if record.type == types.MX:
        (preference,) = struct.unpack_from("!H", record.data, 0)
        exchange, _ = domain_names.unpack_from(record.data, 2)
        return f"{preference} {absolute(exchange)}"
    raise ValueError(f"record type {record.type} is outside the control subset")


def records(section) -> list:
    return [{"name": absolute(record.name), "type": record.type, "class": record.class_,
             "ttl": record.ttl, "rdata": rdata(record)} for record in section]


def parse_dns(data: bytes) -> dict:
    if not data or len(data) > 65535:
        raise ValueError("input outside harness limit")
    message = dns.DNSMessage.unpack(data)
    questions = [{"name": absolute(item.name), "type": item.type, "class": item.class_}
                 for item in message.questions]
    answers, authority = records(message.answers), records(message.authorities)
    additional = records(message.additionals)
    # mitmproxy keeps the 3-bit field after RA as `reserved`; section counts are the parsed list lengths.
    return {"id": message.id, "qr": int(not message.query), "opcode": message.op_code,
            "aa": int(message.authoritative_answer), "tc": int(message.truncation),
            "rd": int(message.recursion_desired), "ra": int(message.recursion_available),
            "z": message.reserved, "rcode": message.response_code, "qdcount": len(questions),
            "ancount": len(answers), "nscount": len(authority), "arcount": len(additional),
            "questions": questions, "answers": answers, "authority": authority, "additional": additional}


def fuzz_one_input(data: bytes):
    try:
        parse_dns(data)
    except Exception:  # mitmproxy raises struct.error, UnicodeDecodeError or ValueError on bad input
        pass
