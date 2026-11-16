# napari-netpbmfile — ASCII PNM / Python

Pinned release: `0.0.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/python/napari-netpbmfile/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm python napari_netpbmfile
python3 parsarium.py run ascii_pnm python napari_netpbmfile controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm python napari_netpbmfile CORPUS_DIR runs/ascii_pnm-napari_netpbmfile-replay
python3 parsarium.py afl build ascii_pnm python napari_netpbmfile
python3 parsarium.py afl prepare ascii_pnm python napari_netpbmfile runs/ascii_pnm-napari_netpbmfile-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
