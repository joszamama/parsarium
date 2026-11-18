# hns-dns-wire — DNS / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.2.2`
- **Upstream:** [source repository](<https://github.com/handshake-rs/hns-dane-engine>) · [crates.io](<https://crates.io/crates/hns-dns-wire>)
- **License:** MIT OR Apache-2.0
- **Parser family:** hns-dns-wire (single-file strict decoder, src/lib.rs)
- **Local input API:** `hns_dns_wire::Message::parse(message: &[u8]) -> Result<Message, Error>`
- **Documentation:** [API reference](<https://docs.rs/hns-dns-wire/0.2.2/hns_dns_wire/struct.Message.html#method.parse>)
- **Valid control:** [`controls/dns/response.bin`](../../../../controls/dns/response.bin)
- **Catalog evidence:** [parser record](../../../../data/rust/dns/parsers.json) · [control result](../../../../data/rust/dns/verification.json)

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
python3 parsarium.py build dns rust hns_dns_wire
python3 parsarium.py run dns rust hns_dns_wire controls/dns/response.bin
```
