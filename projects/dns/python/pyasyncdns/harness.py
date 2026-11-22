"""PyAsyncDNS wire codec over local DNS message bytes through PyAsyncDNS.codec.DNSCodec.decode."""

from PyAsyncDNS.codec import DNSCodec
from PyAsyncDNS.datatypes import AAAARecord, ARecord, CNAMERecord, MXRecord, NSRecord, PTRRecord, TXTRecord

CODEC = DNSCodec()


def absolute(name) -> str:
    text = str(name).lower()
    return text if text.endswith(".") else text + "."


def rdata(record) -> str:
    # Each value is a field of the typed RDATA object DNSCodec built for the record type; the codec
    # falls back to raw bytes when a decoder fails, which the harness rejects.
    value = record.rdata
    if isinstance(value, (ARecord, AAAARecord)):
        return value.address
    if isinstance(value, CNAMERecord):
        return absolute(value.target)
    if isinstance(value, NSRecord):
        return absolute(value.nameserver)
    if isinstance(value, PTRRecord):
        return absolute(value.ptrdname)
    if isinstance(value, MXRecord):
        return f"{int(value.preference)} {absolute(value.exchange)}"
    if isinstance(value, TXTRecord):
        return " ".join('"' + bytes(item).decode("latin-1") + '"' for item in value.strings)
    raise ValueError(f"record type {record.rtype} ({type(value).__name__}) is outside the control subset")


def records(section) -> list:
    return [{"name": absolute(item.name), "type": int(item.rtype), "class": int(item.rclass),
             "ttl": int(item.ttl), "rdata": rdata(item)} for item in section]


def parse_dns(data: bytes) -> dict:
    if not data or len(data) > 65535:
        raise ValueError("input outside harness limit")
    message = CODEC.decode(data)
    header = message.header
    flags = header.flags
    questions = [{"name": absolute(item.name), "type": int(item.qtype), "class": int(item.qclass)}
                 for item in message.questions]
    return {"id": int(header.transaction_id), "qr": int(flags.qr), "opcode": int(flags.opcode), "aa": int(flags.aa),
            "tc": int(flags.tc), "rd": int(flags.rd), "ra": int(flags.ra), "z": int(flags.z),
            "rcode": int(flags.rcode), "qdcount": int(header.question_count), "ancount": int(header.answer_count),
            "nscount": int(header.authority_count), "arcount": int(header.additional_count), "questions": questions,
            "answers": records(message.answers), "authority": records(message.authorities),
            "additional": records(message.additionals)}


def fuzz_one_input(data: bytes):
    try:
        parse_dns(data)
    except Exception:  # the codec raises ValueError, struct.error and others on input it drops
        pass
