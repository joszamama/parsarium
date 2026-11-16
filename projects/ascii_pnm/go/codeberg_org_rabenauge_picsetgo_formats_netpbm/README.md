# codeberg.org/rabenauge/picsetgo/formats/netpbm — ASCII PNM / Go

Pinned release: `v0.5.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/go/codeberg-org-rabenauge-picsetgo-formats-netpbm/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm go codeberg_org_rabenauge_picsetgo_formats_netpbm
python3 parsarium.py run ascii_pnm go codeberg_org_rabenauge_picsetgo_formats_netpbm controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm go codeberg_org_rabenauge_picsetgo_formats_netpbm CORPUS_DIR runs/ascii_pnm-codeberg_org_rabenauge_picsetgo_formats_netpbm-replay
python3 parsarium.py afl build ascii_pnm go codeberg_org_rabenauge_picsetgo_formats_netpbm
python3 parsarium.py afl prepare ascii_pnm go codeberg_org_rabenauge_picsetgo_formats_netpbm runs/ascii_pnm-codeberg_org_rabenauge_picsetgo_formats_netpbm-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
