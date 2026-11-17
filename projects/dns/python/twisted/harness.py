"""Twisted Names decoder over local DNS message bytes through twisted.names.dns.Message.fromStr."""

import ipaddress

from twisted.names import dns


def absolute(name) -> str:
    text = name.name.decode("ascii").lower()
    return text if text.endswith(".") else text + "."


def rdata(payload) -> str:
    # Names, the MX preference, TXT strings and the A dotted quad come from the decoded Record_* objects.
    # Record_AAAA keeps the 16 decoded address bytes; the harness prints them as RFC 5952 text.
    if isinstance(payload, dns.Record_A):
        return payload.dottedQuad()
    if isinstance(payload, dns.Record_AAAA):
        return str(ipaddress.IPv6Address(payload.address))
    if isinstance(payload, (dns.Record_CNAME, dns.Record_NS, dns.Record_PTR)):
        return absolute(payload.name)
    if isinstance(payload, dns.Record_MX):
        return f"{payload.preference} {absolute(payload.name)}"
    if isinstance(payload, dns.Record_TXT):
        return " ".join('"' + item.decode("latin-1") + '"' for item in payload.data)
    raise ValueError(f"record {type(payload).__name__} is outside the control subset")


def records(section) -> list:
    return [{"name": absolute(record.name), "type": record.type, "class": record.cls,
             "ttl": record.ttl, "rdata": rdata(record.payload)} for record in section]


def parse_dns(data: bytes) -> dict:
    if not data or len(data) > 65535:
        raise ValueError("input outside harness limit")
    message = dns.Message()
    message.fromStr(data)
    questions = [{"name": absolute(query.name), "type": query.type, "class": query.cls}
                 for query in message.queries]
    answers, authority = records(message.answers), records(message.authority)
    additional = records(message.additional)
    # Twisted decodes AD and CD but drops the reserved Z bit, so z carries AD and CD only.
    # Section counts are the parsed list lengths.
    return {"id": message.id, "qr": message.answer, "opcode": message.opCode, "aa": message.auth,
            "tc": message.trunc, "rd": message.recDes, "ra": message.recAv,
            "z": (message.authenticData << 1) | message.checkingDisabled,
            "rcode": message.rCode, "qdcount": len(questions), "ancount": len(answers),
            "nscount": len(authority), "arcount": len(additional), "questions": questions,
            "answers": answers, "authority": authority, "additional": additional}


def fuzz_one_input(data: bytes):
    try:
        parse_dns(data)
    except Exception:  # Twisted raises EOFError, DNSDecodeError, struct.error or ValueError on bad input
        pass
