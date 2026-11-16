# netpbm — ASCII PNM / C

Pinned release: `11.02.30`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/c/netpbm/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm c netpbm
python3 parsarium.py run ascii_pnm c netpbm controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm c netpbm CORPUS_DIR runs/ascii_pnm-netpbm-replay
python3 parsarium.py afl build ascii_pnm c netpbm
python3 parsarium.py afl prepare ascii_pnm c netpbm runs/ascii_pnm-netpbm-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
