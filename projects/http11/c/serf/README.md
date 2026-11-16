# serf — HTTP/1.1 / C

Pinned release: `1.3.10`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/c/serf/README.md)

This C harness feeds response bytes through `serf_bucket_simple_create` and `serf_bucket_response_create`, then reads the status line, `Content-Type`, and body. It rejects inputs over 1 MiB and inflated bodies over 4 MiB. It runs the same Apache Serf response parser as the [C++ path](../../cpp/serf/README.md), so the two are one parser family, not two independent engines.

The pinned Docker control parsed an HTTP/1.1 200 response with its reason, Content-Type, and body. LLVM coverage reached 441 Serf bucket source lines, including 153 in `response_buckets.c`; AFL++ reported 461 feedback edges.

## Run from the repository root

```sh
python3 parsarium.py build http11 c serf
python3 parsarium.py run http11 c serf controls/http11/response_serf.http
python3 parsarium.py replay http11 c serf CORPUS_DIR runs/http11-serf-c-replay
python3 parsarium.py afl build http11 c serf
python3 parsarium.py afl prepare http11 c serf runs/http11-serf-c-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
