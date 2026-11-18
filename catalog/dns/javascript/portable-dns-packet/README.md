# @portable/dns-packet — DNS / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.1.0`
- **Upstream:** [source repository](<https://github.com/portablejs/portable>) · [npm](<https://www.npmjs.com/package/@portable/dns-packet>)
- **License:** MIT
- **Parser family:** @portable/dns-packet own decoder (dist/packet.js, wire.js, records.js)
- **Local input API:** `decode(bytes: Uint8Array, options?) -> DecodedPacket`
- **Documentation:** [API reference](<https://github.com/portablejs/portable/blob/main/packages/dns-packet/README.md>)
- **Valid control:** [`controls/dns/response.bin`](../../../../controls/dns/response.bin)
- **Catalog evidence:** [parser record](../../../../data/javascript/dns/parsers.json) · [control result](../../../../data/javascript/dns/verification.json)

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
python3 parsarium.py build dns javascript portable_dns_packet
python3 parsarium.py run dns javascript portable_dns_packet controls/dns/response.bin
```
