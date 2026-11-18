# simple-dns — DNS / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.13.1`
- **Upstream:** [source repository](<https://github.com/balliegojr/simple-dns>) · [crates.io](<https://crates.io/crates/simple-dns>)
- **License:** MIT
- **Parser family:** simple-dns (src/dns/packet.rs, header.rs, name.rs, rdata/*)
- **Local input API:** `simple_dns::Packet::parse(data: &[u8]) -> Result<Packet, SimpleDnsError>`
- **Documentation:** [API reference](<https://docs.rs/simple-dns/0.13.1/simple_dns/struct.Packet.html#method.parse>)
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
python3 parsarium.py build dns rust simple_dns
python3 parsarium.py run dns rust simple_dns controls/dns/response.bin
```
