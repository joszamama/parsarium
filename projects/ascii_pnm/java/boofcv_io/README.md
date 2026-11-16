# boofcv-io — ASCII PNM / Java

Pinned release: `1.6.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/java/boofcv-io/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm java boofcv_io
python3 parsarium.py run ascii_pnm java boofcv_io controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm java boofcv_io CORPUS_DIR runs/ascii_pnm-boofcv_io-replay
python3 parsarium.py afl build ascii_pnm java boofcv_io
python3 parsarium.py afl prepare ascii_pnm java boofcv_io runs/ascii_pnm-boofcv_io-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
