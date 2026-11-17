"""py3dns decoder over local DNS message bytes through DNS.Lib.MunpackerText and DNS.Lib.DnsResult."""

from DNS import Lib

SUBSET = {1, 2, 5, 12, 15, 16, 28}  # A, NS, CNAME, PTR, MX, TXT, AAAA


def absolute(name: str) -> str:
    text = name.lower()
    return text if text.endswith(".") else text + "."


def rdata(record: dict) -> str:
    kind, data = record["type"], record["data"]
    if kind not in SUBSET:
        raise ValueError(f"record type {kind} is outside the control subset")
    # MunpackerText decodes A as dotted text and AAAA through inet_ntop of the 16 decoded bytes.
    if kind in (1, 28):
        return data
    if kind in (2, 5, 12):
        return absolute(data)
    if kind == 15:
        preference, exchange = data
        return f"{preference} {absolute(exchange)}"
    return " ".join(f'"{item}"' for item in data)


def records(section: list) -> list:
    return [{"name": absolute(record["name"]), "type": record["type"], "class": record["class"],
             "ttl": record["ttl"], "rdata": rdata(record)} for record in section]


def parse_dns(data: bytes) -> dict:
    if not data or len(data) > 65535:
        raise ValueError("input outside harness limit")
    # DnsResult.storeM unpacks the header, questions and the three record sections in order;
    # MunpackerText is the unpacker DnsRequest uses for its text result mode.
    result = Lib.DnsResult(Lib.MunpackerText(data), {})
    header = result.header
    questions = [{"name": absolute(item["qname"]), "type": item["qtype"], "class": item["qclass"]}
                 for item in result.questions]
    return {"id": header["id"], "qr": header["qr"], "opcode": header["opcode"], "aa": header["aa"],
            "tc": header["tc"], "rd": header["rd"], "ra": header["ra"], "z": header["z"],
            "rcode": header["rcode"], "qdcount": header["qdcount"], "ancount": header["ancount"],
            "nscount": header["nscount"], "arcount": header["arcount"], "questions": questions,
            "answers": records(result.answers), "authority": records(result.authority),
            "additional": records(result.additional)}


def fuzz_one_input(data: bytes):
    try:
        parse_dns(data)
    except Exception:  # py3dns raises UnpackError, IndexError and struct.error on malformed input
        pass
