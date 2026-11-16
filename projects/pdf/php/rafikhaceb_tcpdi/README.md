# rafikhaceb/tcpdi — PDF / PHP

Pinned release: `2.0.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/php/rafikhaceb-tcpdi/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf php rafikhaceb_tcpdi
python3 parsarium.py run pdf php rafikhaceb_tcpdi controls/pdf/one-page.pdf
python3 parsarium.py replay pdf php rafikhaceb_tcpdi CORPUS_DIR runs/pdf-rafikhaceb_tcpdi-replay
python3 parsarium.py afl build pdf php rafikhaceb_tcpdi
python3 parsarium.py afl prepare pdf php rafikhaceb_tcpdi runs/pdf-rafikhaceb_tcpdi-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
