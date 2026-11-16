# @jdmichaud/netpbm — ASCII PNM / JavaScript

Pinned release: `0.2.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/javascript/jdmichaud-netpbm/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm javascript jdmichaud_netpbm
python3 parsarium.py run ascii_pnm javascript jdmichaud_netpbm controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm javascript jdmichaud_netpbm CORPUS_DIR runs/ascii_pnm-jdmichaud_netpbm-replay
python3 parsarium.py afl build ascii_pnm javascript jdmichaud_netpbm
python3 parsarium.py afl prepare ascii_pnm javascript jdmichaud_netpbm runs/ascii_pnm-jdmichaud_netpbm-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
