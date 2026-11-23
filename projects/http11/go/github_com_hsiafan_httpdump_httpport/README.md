# github.com/hsiafan/httpdump/httpport — HTTP/1.1 / Go

Pinned release: `v0.0.0-20231019014708-4fd809447b59`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/go/github-com-hsiafan-httpdump-httpport/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 go github_com_hsiafan_httpdump_httpport
python3 parsarium.py run http11 go github_com_hsiafan_httpdump_httpport controls/http11/request.http
python3 parsarium.py replay http11 go github_com_hsiafan_httpdump_httpport CORPUS_DIR runs/http11-github_com_hsiafan_httpdump_httpport-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build http11 go github_com_hsiafan_httpdump_httpport
python3 parsarium.py afl prepare http11 go github_com_hsiafan_httpdump_httpport runs/http11-github_com_hsiafan_httpdump_httpport-afl --fandango 100
python3 parsarium.py afl run runs/http11-github_com_hsiafan_httpdump_httpport-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
