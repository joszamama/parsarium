# twisted — DNS / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `26.10.0`
- **Upstream:** [source repository](<https://github.com/twisted/twisted>) · [PyPI](<https://pypi.org/project/twisted/>)
- **License:** MIT
- **Parser family:** Twisted Names (twisted/names/dns.py Message.decode, Query, RRHeader, Name and per-type Record_* decoders)
- **Local input API:** `twisted.names.dns.Message().fromStr(str: bytes) -> None (then the decoded Message fields)`
- **Documentation:** [API reference](<https://docs.twisted.org/en/twisted-26.10.0/api/twisted.names.dns.Message.html#fromStr>)
- **Valid control:** [`controls/dns/response.bin`](../../../../controls/dns/response.bin)
- **Catalog evidence:** [parser record](../../../../data/python/dns/parsers.json) · [control result](../../../../data/python/dns/verification.json)

## Observed control result

```json
{
  "id": 43981,
  "qr": 1,
  "opcode": 0,
  "aa": 0,
  "tc": 0,
  "rd": 1,
  "ra": 1,
  "z": 0,
  "rcode": 0,
  "qdcount": 1,
  "ancount": 4,
  "nscount": 0,
  "arcount": 0,
  "questions": [
    {
      "name": "www.example.test.",
      "type": 1,
      "class": 1
    }
  ],
  "answers": [
    {
      "name": "www.example.test.",
      "type": 5,
      "class": 1,
      "ttl": 3600,
      "rdata": "example.test."
    },
    {
      "name": "example.test.",
      "type": 1,
      "class": 1,
      "ttl": 300,
      "rdata": "192.0.2.10"
    },
    {
      "name": "example.test.",
      "type": 28,
      "class": 1,
      "ttl": 600,
      "rdata": "2001:db8::10"
    },
    {
      "name": "example.test.",
      "type": 15,
      "class": 1,
      "ttl": 7200,
      "rdata": "10 mail.example.test."
    }
  ],
  "authority": [],
  "additional": []
}
```

## Run this target

```sh
python3 parsarium.py build dns python twisted
python3 parsarium.py run dns python twisted controls/dns/response.bin
```
