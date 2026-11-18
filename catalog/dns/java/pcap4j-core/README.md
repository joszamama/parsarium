# pcap4j-core — DNS / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.8.2`
- **Upstream:** [source repository](<https://github.com/kaitoy/pcap4j>) · [Maven Central](<https://central.sonatype.com/artifact/org.pcap4j/pcap4j-core>)
- **License:** MIT
- **Parser family:** Pcap4J DNS packet classes (DnsPacket, DnsDomainName, DnsResourceRecord, DnsRData*)
- **Local input API:** `org.pcap4j.packet.DnsPacket.newPacket(byte[] rawData, int offset, int length) throws IllegalRawDataException`
- **Documentation:** [API reference](<https://javadoc.io/doc/org.pcap4j/pcap4j-core/1.8.2/org/pcap4j/packet/DnsPacket.html>)
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
python3 parsarium.py build dns java pcap4j_core
python3 parsarium.py run dns java pcap4j_core controls/dns/response.bin
```
