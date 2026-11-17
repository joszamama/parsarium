# glibc libresolv ns_initparse/ns_parserr — DNS / C

**Pilot / incomplete format cell.**

- **Runtime:** glibc 2.43 libresolv (Ubuntu 2.43-2ubuntu2.7, linux/arm64, ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96)
- **Parser family:** BIND 8 libresolv ns_parse (glibc resolv/ns_parse.c, ns_name.c)
- **Official documentation:** [reference](https://sourceware.org/git/?p=glibc.git;a=blob;f=resolv/arpa/nameser.h)
- **Valid control:** [`controls/dns/response.bin`](../../../../../controls/dns/response.bin)
- **Inventory:** [standard API record](../../../../../data/c/dns/standard.json) · [saved result](../../../../../data/c/dns/libresolv-standard-result.json)

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
