# getdns — DNS / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.7.3`
- **Upstream:** [source repository](<https://github.com/getdnsapi/getdns>) · [Debian](<https://tracker.debian.org/pkg/getdns>)
- **License:** BSD-3-Clause
- **Parser family:** getdns message-dict decoder (src/rr-iter.c, src/rr-dict.c, src/util-internal.c over the bundled gldns read helpers)
- **Local input API:** `getdns_return_t getdns_wire2msg_dict(const uint8_t *wire, size_t wire_sz, getdns_dict **msg_dict)`
- **Documentation:** [API reference](<https://getdnsapi.net/doxygen/group__UDNSDataConversionFunctions.html>)
- **Valid control:** [`controls/dns/response.bin`](../../../../controls/dns/response.bin)
- **Catalog evidence:** [parser record](../../../../data/c/dns/parsers.json) · [control result](../../../../data/c/dns/verification.json)

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
python3 parsarium.py build dns c getdns
python3 parsarium.py run dns c getdns controls/dns/response.bin
```
