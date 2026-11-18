# wahern-dns — DNS / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `rel-20160808`
- **Upstream:** [source repository](<https://github.com/wahern/dns>)
- **License:** MIT
- **Parser family:** dns.c (William Ahern) single-file packet decoder (src/dns.c)
- **Local input API:** `struct dns_packet *dns_p_make(size_t, int *) filled with the message bytes (P->data, P->end), int dns_p_study(struct dns_packet *), dns_header(P) and dns_p_count(P, section), then dns_rr_grep via dns_rr_foreach(&rr, P, .section = ..., .sort = dns_rr_i_packet); names from dns_d_expand, RDATA from dns_any_parse + dns_any_print`
- **Documentation:** [API reference](<https://github.com/wahern/dns/blob/rel-20160808/README.md>)
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
python3 parsarium.py build dns c wahern-dns
python3 parsarium.py run dns c wahern-dns controls/dns/response.bin
```
