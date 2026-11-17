"""dns-messages decoder over local DNS message bytes through dns_messages.DnsMessage.from_bytes."""

from dns_messages import AAAA, CNAME, MX, PTR, TXT, A, DnsMessage


def absolute(name: str) -> str:
    text = name.lower()
    return text if text.endswith(".") else text + "."


def rdata(record) -> str:
    # str() of the ipaddress objects the library builds from the decoded address bytes gives the
    # dotted quad and RFC 5952 text; names and the MX preference are the library's own fields.
    if isinstance(record, (A, AAAA)):
        return str(record.ip_address)
    if isinstance(record, CNAME):
        return absolute(record.domain_name)
    if isinstance(record, PTR):
        return absolute(record.domain_name)
    if isinstance(record, MX):
        return f"{record.preference} {absolute(record.exchange)}"
    if isinstance(record, TXT):
        return " ".join('"' + item.decode("latin-1") + '"' for item in record.text_lines)
    raise ValueError(f"record {type(record).__name__} is outside the control subset")


def records(section) -> list:
    return [{"name": absolute(record.name), "type": record.get_RR_type().value,
             "class": record.rr_class.value, "ttl": record.ttl, "rdata": rdata(record)} for record in section]


def parse_dns(data: bytes) -> dict:
    if not data or len(data) > 65535:
        raise ValueError("input outside harness limit")
    message = DnsMessage.from_bytes(data)
    questions = [{"name": absolute(item.name), "type": item.rr_type.value, "class": item.rr_class.value}
                 for item in message.questions]
    answers, authority = records(message.answers_RRs), records(message.authority_RRs)
    additional = records(message.additional_RRs)
    # The parser keeps the 3-bit z field after RA; section counts are the parsed list lengths.
    return {"id": message.message_id, "qr": message.qr, "opcode": message.op_code.value, "aa": message.aa,
            "tc": message.tc, "rd": message.rd, "ra": message.ra, "z": message.z,
            "rcode": message.rcode.value, "qdcount": len(questions), "ancount": len(answers),
            "nscount": len(authority), "arcount": len(additional), "questions": questions,
            "answers": answers, "authority": authority, "additional": additional}


def fuzz_one_input(data: bytes):
    try:
        parse_dns(data)
    except Exception:  # dns-messages wraps parse failures in DnsPacketParsingException
        pass
