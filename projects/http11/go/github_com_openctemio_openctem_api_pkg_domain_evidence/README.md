# github.com/openctemio/openctem/api/pkg/domain/evidence — HTTP/1.1 / Go

Pinned release: `v0.0.0-20261107202920-27e7faec6f5d`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/go/github-com-openctemio-openctem-api-pkg-domain-evidence/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 go github_com_openctemio_openctem_api_pkg_domain_evidence
python3 parsarium.py run http11 go github_com_openctemio_openctem_api_pkg_domain_evidence controls/http11/request.http
python3 parsarium.py replay http11 go github_com_openctemio_openctem_api_pkg_domain_evidence CORPUS_DIR runs/http11-github_com_openctemio_openctem_api_pkg_domain_evidence-replay
python3 parsarium.py afl build http11 go github_com_openctemio_openctem_api_pkg_domain_evidence
python3 parsarium.py afl prepare http11 go github_com_openctemio_openctem_api_pkg_domain_evidence runs/http11-github_com_openctemio_openctem_api_pkg_domain_evidence-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
