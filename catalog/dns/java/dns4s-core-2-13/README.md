# dns4s-core_2.13 — DNS / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.21.0`
- **Upstream:** [source repository](<https://github.com/mkroli/dns4s>) · [Maven Central](<https://central.sonatype.com/artifact/com.github.mkroli/dns4s-core_2.13>)
- **License:** Apache-2.0
- **Parser family:** dns4s (Scala: Message, MessageBuffer, HeaderSection, QuestionSection, ResourceRecord and section.resource decoders)
- **Local input API:** `com.github.mkroli.dns4s.Message.apply(bytes: MessageBuffer): Message, with MessageBuffer.apply(buf: java.nio.ByteBuffer) (Scala companion objects, called from Java as Message$.MODULE$ and MessageBuffer$.MODULE$)`
- **Documentation:** [API reference](<https://mkroli.github.io/dns4s/api/com/github/mkroli/dns4s/Message$.html>)
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
python3 parsarium.py build dns java dns4s_core
python3 parsarium.py run dns java dns4s_core controls/dns/response.bin
```
