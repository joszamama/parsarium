# xibalba-proto — HTTP/1.1 / Rust

- **Pinned release:** `0.4.0`
- **License:** MIT
- **Parsed scope:** response head: status and fields; body slice after consumed offset
- **Underlying family:** xibalba-proto
- **Local input API:** `ResponseHead::parse(&bytes, &mut header_slots)`
- **Documentation:** [API reference](<https://docs.rs/xibalba-proto/0.4.0/xibalba_proto/>)
- **Catalog evidence:** [parser record](../../../../data/rust/http11/parsers.json) · [control verification](../../../../data/rust/http11/verification.json) · [within-ecosystem ranking](../../../../data/rust/http11/ranking.md)
- **Valid control:** [`controls/http11/response.http`](../../../../controls/http11/response.http)

## Observed control result

```json
{
  "body": "parsarium",
  "headers": 2,
  "status": 200
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/rust/xibalba_proto/README.md)

```sh
python3 parsarium.py build http11 rust xibalba_proto
python3 parsarium.py run http11 rust xibalba_proto controls/http11/response.http
```
