# propa/tcpdi — PDF / PHP

Pinned release: `v1.3.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/php/propa-tcpdi/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf php propa_tcpdi
python3 parsarium.py run pdf php propa_tcpdi controls/pdf/one-page.pdf
python3 parsarium.py replay pdf php propa_tcpdi CORPUS_DIR runs/pdf-propa_tcpdi-replay
python3 parsarium.py afl build pdf php propa_tcpdi
python3 parsarium.py afl prepare pdf php propa_tcpdi runs/pdf-propa_tcpdi-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
