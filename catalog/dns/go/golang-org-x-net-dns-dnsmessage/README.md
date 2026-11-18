# golang.org/x/net/dns/dnsmessage — DNS / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v0.63.0`
- **Upstream:** [source repository](<https://go.googlesource.com/net>) · [pkg.go.dev](<https://pkg.go.dev/golang.org/x/net/dns/dnsmessage>)
- **License:** BSD-3-Clause
- **Parser family:** Go x/net dnsmessage (dns/dnsmessage/message.go)
- **Local input API:** `(*dnsmessage.Message).Unpack(msg []byte) error`
- **Documentation:** [API reference](<https://pkg.go.dev/golang.org/x/net@v0.63.0/dns/dnsmessage#Message.Unpack>)
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
python3 parsarium.py build dns go golang_org_x_net_dns_dnsmessage
python3 parsarium.py run dns go golang_org_x_net_dns_dnsmessage controls/dns/response.bin
```
