# netpbm-parser — ASCII PNM / JavaScript

Pinned release: `1.1.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/javascript/netpbm-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm javascript netpbm_parser
python3 parsarium.py run ascii_pnm javascript netpbm_parser controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm javascript netpbm_parser CORPUS_DIR runs/ascii_pnm-netpbm_parser-replay
python3 parsarium.py afl build ascii_pnm javascript netpbm_parser
python3 parsarium.py afl prepare ascii_pnm javascript netpbm_parser runs/ascii_pnm-netpbm_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
