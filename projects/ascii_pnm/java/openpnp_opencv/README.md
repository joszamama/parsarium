# openpnp-opencv — ASCII PNM / Java

Pinned release: `4.9.0-0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/java/openpnp-opencv/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm java openpnp_opencv
python3 parsarium.py run ascii_pnm java openpnp_opencv controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm java openpnp_opencv CORPUS_DIR runs/ascii_pnm-openpnp_opencv-replay
python3 parsarium.py afl build ascii_pnm java openpnp_opencv
python3 parsarium.py afl prepare ascii_pnm java openpnp_opencv runs/ascii_pnm-openpnp_opencv-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
