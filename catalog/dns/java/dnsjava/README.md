# dnsjava — DNS / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `3.7.1`
- **Upstream:** [source repository](<https://github.com/dnsjava/dnsjava>) · [Maven Central](<https://central.sonatype.com/artifact/dnsjava/dnsjava>)
- **License:** BSD-3-Clause
- **Parser family:** dnsjava (org.xbill.DNS Message, Header, DNSInput, Name and per-type rrFromWire)
- **Local input API:** `org.xbill.DNS.Message(byte[] b) throws IOException`
- **Documentation:** [API reference](<https://javadoc.io/doc/dnsjava/dnsjava/3.7.1/org/xbill/DNS/Message.html#%3Cinit%3E(byte%5B%5D)>)
- **Valid control:** [`controls/dns/response.bin`](../../../../controls/dns/response.bin)
- **Catalog evidence:** [parser record](../../../../data/java/dns/parsers.json) · [control result](../../../../data/java/dns/verification.json)

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
python3 parsarium.py build dns java dnsjava
python3 parsarium.py run dns java dnsjava controls/dns/response.bin
```
