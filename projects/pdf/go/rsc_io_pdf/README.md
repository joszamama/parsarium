# rsc.io/pdf — PDF / Go

Pinned release: `v0.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/go/rsc-io-pdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf go rsc_io_pdf
python3 parsarium.py run pdf go rsc_io_pdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf go rsc_io_pdf CORPUS_DIR runs/pdf-rsc_io_pdf-replay
python3 parsarium.py afl build pdf go rsc_io_pdf
python3 parsarium.py afl prepare pdf go rsc_io_pdf runs/pdf-rsc_io_pdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
