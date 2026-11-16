# github.com/projectdiscovery/nuclei/v3/pkg/protocols/http/raw — HTTP/1.1 / Go

Pinned release: `v3.11.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/go/github-com-projectdiscovery-nuclei-v3-pkg-protocols-http-raw/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 go github_com_projectdiscovery_nuclei_v3_pkg_protocols_http_raw
python3 parsarium.py run http11 go github_com_projectdiscovery_nuclei_v3_pkg_protocols_http_raw controls/http11/request.http
python3 parsarium.py replay http11 go github_com_projectdiscovery_nuclei_v3_pkg_protocols_http_raw CORPUS_DIR runs/http11-github_com_projectdiscovery_nuclei_v3_pkg_protocols_http_raw-replay
python3 parsarium.py afl build http11 go github_com_projectdiscovery_nuclei_v3_pkg_protocols_http_raw
python3 parsarium.py afl prepare http11 go github_com_projectdiscovery_nuclei_v3_pkg_protocols_http_raw runs/http11-github_com_projectdiscovery_nuclei_v3_pkg_protocols_http_raw-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
