# udns — DNS / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.7`
- **Upstream:** [Debian](<https://tracker.debian.org/pkg/udns>)
- **License:** LGPL-2.1-or-later
- **Parser family:** udns (Michael Tokarev) raw-packet routines (udns_parse.c, udns_dn.c, udns_XtoX.c)
- **Local input API:** `dns_getdn(pkt, &cur, end, dn, dnsiz) for question names, then void dns_initparse(struct dns_parse *p, dnscc_t *qdn, dnscc_t *pkt, dnscc_t *cur, dnscc_t *end) + int dns_nextrr(struct dns_parse *p, struct dns_rr *rr), with the dns_qid/dns_qr/.../dns_numar header accessors`
- **Documentation:** [API reference](<https://www.corpit.ru/mjt/udns/udns.3.html>)
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
python3 parsarium.py build dns c udns
python3 parsarium.py run dns c udns controls/dns/response.bin
```
