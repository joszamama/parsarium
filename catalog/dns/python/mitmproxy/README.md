# mitmproxy — DNS / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `12.3.1`
- **License:** MIT
- **Parser family:** mitmproxy DNS (mitmproxy/dns.py DNSMessage.unpack_from over mitmproxy/net/dns/domain_names.py)
- **Local input API:** `mitmproxy.dns.DNSMessage.unpack(buffer: bytes, timestamp: float | None = None) -> DNSMessage`
- **Documentation:** [API reference](<https://docs.mitmproxy.org/stable/api/mitmproxy/dns.html#DNSMessage.unpack>)
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
python3 parsarium.py build dns python mitmproxy
python3 parsarium.py run dns python mitmproxy controls/dns/response.bin
```
