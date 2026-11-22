"""pydns3 message codec over local DNS message bytes through pydns.Message.unpack."""

from pydns import Message


def absolute(name) -> str:
    text = (name.decode("ascii") if isinstance(name, (bytes, bytearray)) else str(name)).lower()
    return text if text.endswith(".") else text + "."


def rdata(answer) -> str:
    # Each value is a field of the typed content object pydns built for the record type
    # (A/AAAA ip, CNAME name, NS nameserver, PTR ptrname, MX preference and exchange).
    rtype = int(answer.rtype)
    content = answer.content
    if rtype in (1, 28):
        return str(content.ip)
    if rtype == 5:
        return absolute(content.name)
    if rtype == 2:
        return absolute(content.nameserver)
    if rtype == 12:
        return absolute(content.ptrname)
    if rtype == 15:
        return f"{int(content.preference)} {absolute(content.exchange)}"
    if rtype == 16:
        # pydns.content.TXT keeps one text blob.
        return '"' + bytes(content.text).decode("latin-1") + '"'
    raise ValueError(f"record type {rtype} is outside the control subset")


def records(section) -> list:
    return [{"name": absolute(answer.name), "type": int(answer.rtype), "class": int(answer.rclass),
             "ttl": int(answer.ttl), "rdata": rdata(answer)} for answer in section]


def parse_dns(data: bytes) -> dict:
    if not data or len(data) > 65535:
        raise ValueError("input outside harness limit")
    message = Message.unpack(data)
    flags = message.flags
    questions = [{"name": absolute(item.name), "type": int(item.qtype), "class": int(item.qclass)}
                 for item in message.questions]
    # pydns.Flags keeps AD (answer_authenticated) and CD (checking_disabled) but drops the reserved
    # Z bit, so z carries AD and CD only.
    z = int(flags.answer_authenticated) << 1 | int(flags.checking_disabled)
    return {"id": int(message.id), "qr": int(flags.qr), "opcode": int(flags.op), "aa": int(flags.authorative),
            "tc": int(flags.truncated), "rd": int(flags.recursion_desired), "ra": int(flags.recursion_available),
            "z": z, "rcode": int(flags.rcode), "qdcount": len(message.questions), "ancount": len(message.answers),
            "nscount": len(message.authority), "arcount": len(message.additional), "questions": questions,
            "answers": records(message.answers), "authority": records(message.authority),
            "additional": records(message.additional)}


def fuzz_one_input(data: bytes):
    try:
        parse_dns(data)
    except Exception:  # pydns and pystructs raise ValueError, IndexError and others on input they drop
        pass
