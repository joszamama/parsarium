# serf — HTTP/1.1 / C

Pinned release: `1.3.10`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/c/serf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 c serf
python3 parsarium.py run http11 c serf controls/http11/response_serf.http
python3 parsarium.py replay http11 c serf CORPUS_DIR runs/http11-serf-replay
python3 parsarium.py afl build http11 c serf
python3 parsarium.py afl prepare http11 c serf runs/http11-serf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
