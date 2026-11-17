# serf — HTTP/1.1 / C

- **Pinned release:** `1.3.10`
- **License:** Apache-2.0
- **Parsed scope:** HTTP/1.1 response status, reason, Content-Type, Content-Length and body from local byte buffer
- **Underlying family:** Apache Serf C HTTP/1 response bucket state machine; independent from libsoup and llhttp
- **Local input API:** `serf_bucket_simple_create(local response bytes); serf_bucket_response_create(stream); serf_bucket_response_status/wait_for_headers/get_headers and serf_bucket_read`
- **Documentation:** [API reference](<https://github.com/apache/serf/blob/1.3.10/serf_bucket_types.h>)
- **Catalog evidence:** [parser record](../../../../data/c/http11/parsers.json) · [control verification](../../../../data/c/http11/verification.json) · [within-ecosystem ranking](../../../../data/c/http11/ranking.md)
- **Valid control:** [`controls/http11/response_serf.http`](../../../../controls/http11/response_serf.http)

## Observed control result

```json
{
  "version": "1.1",
  "status": 200,
  "reason": "OK",
  "content_type": "text/plain",
  "body": "OK"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/c/serf/README.md)

```sh
python3 parsarium.py build http11 c serf
python3 parsarium.py run http11 c serf controls/http11/response_serf.http
```
