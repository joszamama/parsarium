# andreaventuri/tcpdi — PDF / PHP

Pinned release: `1.0.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/php/andreaventuri-tcpdi/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf php andreaventuri_tcpdi
python3 parsarium.py run pdf php andreaventuri_tcpdi controls/pdf/one-page.pdf
python3 parsarium.py replay pdf php andreaventuri_tcpdi CORPUS_DIR runs/pdf-andreaventuri_tcpdi-replay
python3 parsarium.py afl build pdf php andreaventuri_tcpdi
python3 parsarium.py afl prepare pdf php andreaventuri_tcpdi runs/pdf-andreaventuri_tcpdi-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
