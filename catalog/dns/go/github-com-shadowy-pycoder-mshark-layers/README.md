# github.com/shadowy-pycoder/mshark/layers — DNS / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v0.0.32`
- **Upstream:** [source repository](<https://github.com/shadowy-pycoder/mshark>) · [pkg.go.dev](<https://pkg.go.dev/github.com/shadowy-pycoder/mshark/layers>)
- **License:** MIT
- **Parser family:** mshark layers (dns.go UnmarshalBinary, extractDomain, parseRData)
- **Local input API:** `(*layers.DNSMessage).Parse(data []byte) error (UnmarshalBinary), then DNSMessage.TransactionID, Flags (QR, OPCode, AA, TC, RD, RA, Z, AU, NA, RCode), Questions ([]*QueryEntry) and AnswerRRs/AuthorityRRs/AdditionalRRs ([]*ResourceRecord with typed RDataA, RDataAAAA, RDataCNAME, RDataMX)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/shadowy-pycoder/mshark@v0.0.32/layers#DNSMessage.Parse>)
- **Valid control:** [`controls/dns/response.bin`](../../../../controls/dns/response.bin)
- **Catalog evidence:** [parser record](../../../../data/go/dns/parsers.json) · [control result](../../../../data/go/dns/verification.json)

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
python3 parsarium.py build dns go github_com_shadowy_pycoder_mshark_layers
python3 parsarium.py run dns go github_com_shadowy_pycoder_mshark_layers controls/dns/response.bin
```
