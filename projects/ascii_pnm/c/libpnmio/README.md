# libpnmio — ASCII PNM / C

Pinned release: `1.2.7 (README; commit pinned)`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/c/libpnmio/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm c libpnmio
python3 parsarium.py run ascii_pnm c libpnmio controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm c libpnmio CORPUS_DIR runs/ascii_pnm-libpnmio-replay
python3 parsarium.py afl build ascii_pnm c libpnmio
python3 parsarium.py afl prepare ascii_pnm c libpnmio runs/ascii_pnm-libpnmio-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
