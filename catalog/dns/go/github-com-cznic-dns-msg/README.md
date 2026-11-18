# github.com/cznic/dns/msg — DNS / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v0.0.0-20181122101858-8a2913d6a50b`
- **Upstream:** [source repository](<https://github.com/cznic/dns>) · [pkg.go.dev](<https://pkg.go.dev/github.com/cznic/dns/msg>)
- **License:** BSD-3-Clause
- **Parser family:** cznic/dns (msg/message.go, rr/rr.go, wire.go)
- **Local input API:** `(*msg.Message).Decode(b []byte, pos *int, sniffer dns.WireDecodeSniffer) error`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/cznic/dns@v0.0.0-20181122101858-8a2913d6a50b/msg#Message.Decode>)
- **Valid control:** [`controls/dns/response.bin`](../../../../controls/dns/response.bin)
- **Catalog evidence:** [parser record](../../../../data/go/dns/parsers.json) · [control result](../../../../data/go/dns/verification.json)

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
python3 parsarium.py build dns go github_com_cznic_dns_msg
python3 parsarium.py run dns go github_com_cznic_dns_msg controls/dns/response.bin
```
