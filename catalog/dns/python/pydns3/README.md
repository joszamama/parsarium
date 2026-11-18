# pydns3 — DNS / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.0.10`
- **Upstream:** [source repository](<https://github.com/imgurbot12/pydns>) · [PyPI](<https://pypi.org/project/pydns3/>)
- **License:** MIT
- **Parser family:** pydns3 (message.py Message.unpack, answer.py, content.py) over pystructs3 (std.py Domain name codec, struct.py Struct)
- **Local input API:** `pydns.Message.unpack(raw: bytes, ctx: Optional[pystructs.Context] = None) -> Message (fields id, flags, questions, answers, authority, additional; Answer.content typed A/AAAA/CNAME/MX/NS/PTR/SOA/TXT/SRV)`
- **Documentation:** [API reference](<https://github.com/imgurbot12/pydns/blob/master/README.md>)
- **Valid control:** [`controls/dns/response.bin`](../../../../controls/dns/response.bin)
- **Catalog evidence:** [parser record](../../../../data/python/dns/parsers.json) · [control result](../../../../data/python/dns/verification.json)

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
python3 parsarium.py build dns python pydns3
python3 parsarium.py run dns python pydns3 controls/dns/response.bin
```
