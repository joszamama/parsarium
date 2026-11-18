# pear/net_dns2 — DNS / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v2.0.7`
- **Upstream:** [source repository](<https://github.com/mikepultz/netdns2>) · [Packagist](<https://packagist.org/packages/pear/net_dns2>)
- **License:** MIT
- **Parser family:** Net_DNS2 / NetDNS2 (Packet, Header, Question and per-type RR rrSet decoders)
- **Local input API:** `NetDNS2\Packet\Response::__construct(string $_data, int $_size)`
- **Documentation:** [API reference](<https://github.com/mikepultz/netdns2/blob/v2.0.7/src/NetDNS2/Packet/Response.php>)
- **Valid control:** [`controls/dns/response.bin`](../../../../controls/dns/response.bin)
- **Catalog evidence:** [parser record](../../../../data/php/dns/parsers.json) · [control result](../../../../data/php/dns/verification.json)

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
python3 parsarium.py build dns php pear_net_dns2
python3 parsarium.py run dns php pear_net_dns2 controls/dns/response.bin
```
