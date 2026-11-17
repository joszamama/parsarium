"""dnspython wire-format decoder over local DNS message bytes through dns.message.from_wire."""

import dns.message
import dns.opcode

SECTIONS = ("answers", "authority", "additional")


def absolute(name) -> str:
    text = name.to_text().lower()
    return text if text.endswith(".") else text + "."


def records(section) -> list:
    # dnspython groups records into RRsets; each rdata keeps its RRset's owner, type, class and TTL.
    return [{"name": absolute(rrset.name), "type": int(rrset.rdtype), "class": int(rrset.rdclass),
             "ttl": rrset.ttl, "rdata": rdata.to_text()}
            for rrset in section for rdata in rrset]


def parse_dns(data: bytes) -> dict:
    if not data or len(data) > 65535:
        raise ValueError("input outside harness limit")
    message = dns.message.from_wire(data)
    flags = message.flags
    question = [{"name": absolute(rrset.name), "type": int(rrset.rdtype), "class": int(rrset.rdclass)}
                for rrset in message.question]
    sections = dict(zip(SECTIONS, (records(message.answer), records(message.authority),
                                   records(message.additional))))
    return {"id": message.id, "qr": (flags >> 15) & 1, "opcode": int(dns.opcode.from_flags(flags)),
            "aa": (flags >> 10) & 1, "tc": (flags >> 9) & 1, "rd": (flags >> 8) & 1,
            "ra": (flags >> 7) & 1, "z": (flags >> 4) & 7, "rcode": int(message.rcode()),
            "qdcount": len(question), "ancount": len(sections["answers"]),
            "nscount": len(sections["authority"]), "arcount": len(sections["additional"]),
            "questions": question, **sections}


def fuzz_one_input(data: bytes):
    try:
        parse_dns(data)
    except Exception:  # dnspython raises its own DNSException subclasses on malformed input
        pass
