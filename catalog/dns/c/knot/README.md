# knot — DNS / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `3.6.2`
- **License:** GPL-2.0-or-later
- **Parser family:** Knot DNS libknot (packet/pkt.c, packet/rrset-wire.c, dname.c; rrset-dump.c for presentation)
- **Local input API:** `knot_pkt_t *knot_pkt_new(void *wire, uint16_t len, knot_mm_t *mm) + int knot_pkt_parse(knot_pkt_t *pkt, unsigned flags)`
- **Documentation:** [API reference](<https://gitlab.nic.cz/knot/knot-dns/-/blob/v3.6.2/src/libknot/packet/pkt.h>)
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
python3 parsarium.py build dns c knot
python3 parsarium.py run dns c knot controls/dns/response.bin
```
