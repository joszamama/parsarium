"""namespy wire codec over local DNS message bytes through namespy.DnsPacket.parse."""

from namespy import DnsPacket


def absolute(name) -> str:
    text = str(name).lower()
    return text if text.endswith(".") else text + "."


def rdata(record) -> str:
    # RData.to_presentation() is the library's own presentation text: a dotted quad for A, RFC 5952
    # text for AAAA, the decompressed name for CNAME/NS/PTR and "<preference> <exchange>" for MX.
    rtype = int(record.rtype)
    text = record.rdata.to_presentation()
    if rtype in (2, 5, 12):
        return absolute(text)
    if rtype == 15:
        preference, exchange = text.split(" ", 1)
        return f"{int(preference)} {absolute(exchange)}"
    if rtype in (1, 16, 28):
        return text
    raise ValueError(f"record type {rtype} is outside the control subset")


def records(section) -> list:
    return [{"name": absolute(record.name), "type": int(record.rtype), "class": int(record.rclass),
             "ttl": record.ttl, "rdata": rdata(record)} for record in section]


def parse_dns(data: bytes) -> dict:
    if not data or len(data) > 65535:
        raise ValueError("input outside harness limit")
    packet, consumed = DnsPacket.parse(data)
    if consumed != len(data):
        raise ValueError("trailing octets after the message")
    questions = [{"name": absolute(item.name), "type": int(item.qtype), "class": int(item.qclass)}
                 for item in packet.questions]
    # namespy models the reserved Z bit, AD and CD separately; z joins them as the three bits after RA.
    z = (int(packet.Z) & 1) << 2 | int(packet.AD) << 1 | int(packet.CD)
    return {"id": packet.ID, "qr": int(packet.QR), "opcode": int(packet.OPCODE), "aa": int(packet.AA),
            "tc": int(packet.TC), "rd": int(packet.RD), "ra": int(packet.RA), "z": z,
            "rcode": int(packet.RCODE), "qdcount": packet.QDCOUNT, "ancount": packet.ANCOUNT,
            "nscount": packet.NSCOUNT, "arcount": packet.ARCOUNT, "questions": questions,
            "answers": records(packet.answers), "authority": records(packet.nameservers),
            "additional": records(packet.additional_records)}


def fuzz_one_input(data: bytes):
    try:
        parse_dns(data)
    except Exception:  # namespy raises DnsPacketParseError (a ValueError) on input it drops
        pass
